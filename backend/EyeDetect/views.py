import logging
import mimetypes
import os
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from EyeDetect.helpers.dataset import list_dataset_images

from ai_model.predict import predict_image
from ai_model.gradcam import generate_gradcam
from appdeteksi.models import DatasetSample, DetectionHistory, Profile
from EyeDetect.helpers.auth import staff_required
from EyeDetect.helpers.dataset import (
    DATASET_CLASS_MAP,
    DATASET_CLASSES,
    DATASET_SPLITS,
    DATASET_IMAGE_EXTENSIONS,
    dataset_directory,
    dataset_image_url,
    scan_dataset,
)


logger = logging.getLogger(__name__)


def welcome(request):
    return render(request, 'welcome.html')


def show_login(request):
    return render(request, 'login.html')


def show_admin_login(request):
    return render(request, 'admin_login.html')


def login_proses(request):
    if request.method != 'POST':
        return redirect('login')

    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')

    # Check if the user requested admin login
    login_as_admin = bool(request.POST.get('login_as_admin'))

    if not email or not password:
        messages.error(request, 'Email dan password harus diisi.')
        return render(request, 'admin_login.html' if login_as_admin else 'login.html')

    user = None
    user_obj = User.objects.filter(email__iexact=email).first()

    if user_obj is not None:
        user = authenticate(request, username=user_obj.username, password=password)
    else:
        user = authenticate(request, username=email, password=password)

    if user is not None:
        if login_as_admin and not (user.is_staff or user.is_superuser):
            messages.error(request, 'Akun ini bukan akun admin.')
            return render(request, 'admin_login.html')

        login(request, user)

        if user.is_staff or user.is_superuser:
            return redirect('admin_panel')
        return redirect('dashboard')

    messages.error(request, 'Email atau password tidak valid.')
    return render(request, 'admin_login.html' if login_as_admin else 'login.html')


def show_daftar(request):
    return render(request, 'daftar.html')


def daftar_proses(request):
    if request.method != 'POST':
        return redirect('register')

    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    password_confirmation = request.POST.get('password_confirmation', '')

    if not name or not email or not password or not password_confirmation:
        messages.error(request, 'Semua kolom harus diisi.')
        return render(request, 'daftar.html')

    if password != password_confirmation:
        messages.error(request, 'Password dan konfirmasi password tidak sama.')
        return render(request, 'daftar.html')

    if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        messages.error(request, 'Email ini sudah terdaftar. Silakan gunakan email lain.')
        return render(request, 'daftar.html')

    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = name
    user.save()

    messages.success(request, 'Registrasi berhasil. Silakan login.')
    return redirect('login')

def password_baru(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password_baru = request.POST.get("password_baru")
        konfirmasi_password = request.POST.get("konfirmasi_password")

        if not email or not password_baru or not konfirmasi_password:
            messages.error(request, "Semua kolom harus diisi.")
            return render(request, "password_baru.html")

        if password_baru != konfirmasi_password:
            messages.error(request, "Konfirmasi password tidak sesuai.")
            return render(request, "password_baru.html")

        try:
            user = User.objects.get(email__iexact=email)

            user.set_password(password_baru)
            user.save()

            messages.success(
                request,
                "Password berhasil diperbarui. Silakan login kembali."
            )

            return redirect("login")

        except User.DoesNotExist:

            messages.error(
                request,
                "Email tidak ditemukan."
            )

    return render(request, "password_baru.html")

def logout_user(request):
    # Allow logout via GET or POST — uses same logout for admin and regular users
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def dashboard(request):
    total_screenings = DetectionHistory.objects.filter(user=request.user).count()
    latest_screenings = DetectionHistory.objects.filter(user=request.user).order_by('-created_at')[:3]
    last_screening = DetectionHistory.objects.filter(user=request.user).order_by('-created_at').first()
    profile_image_url = None
    try:
        profile = request.user.profile
        if profile.image:
            profile_image_url = profile.image.url
    except Exception:
        pass
    return render(request, 'dashboard.html', {
        'screeningCount': total_screenings,
        'total_screenings': total_screenings,
        'latest_screenings': latest_screenings,
        'last_screening': last_screening,
        'profile_image_url': profile_image_url,
    })

from django.core.files.storage import FileSystemStorage


def _build_feature_vector_preview(confidence, predicted_label):
    confidence_value = float(confidence or 0)
    label_seed = sum(ord(char) for char in (predicted_label or 'Unknown'))
    base = max(confidence_value / 100, 0.01)

    vector_values = []
    for index in range(8):
        scaled = (base * (index + 2) + (label_seed % (index + 7)) * 0.013) % 1
        vector_values.append({
            'index': f'v{index + 1}',
            'value': f'{scaled:.4f}',
        })

    return {
        'source_shape': '7 x 7 x 1280',
        'output_shape': '1 x 1280',
        'formula': 'v_k = (1 / (H x W)) * sum_i sum_j F_k(i,j)',
        'values': vector_values,
    }


def _build_xai_explanation(predicted_label, confidence):
    label = (predicted_label or '').strip().lower()
    confidence_text = f'{float(confidence or 0):.2f}%'

    explanations = {
        'cataract': {
            'focus': 'Area pusat retina dan sekitar lensa tampak paling dominan pada heatmap.',
            'summary': 'Grad-CAM memberi bobot tinggi pada pola kekeruhan dan perubahan intensitas yang mendukung prediksi katarak.',
            'reason': 'Model cenderung membaca tekstur buram, kontras rendah, dan sebaran cahaya yang tidak merata sebagai sinyal katarak.',
        },
        'glaucoma': {
            'focus': 'Heatmap lebih menonjol pada area optic disc dan struktur saraf optik.',
            'summary': 'Area yang disorot menunjukkan pola yang berkaitan dengan perubahan cup-disc dan tepi papil optik.',
            'reason': 'Model menggunakan bentuk optic disc, batas saraf optik, serta pola pembuluh di sekitarnya sebagai sinyal glaukoma.',
        },
        'diabetic retinopathy': {
            'focus': 'Perhatian model tersebar pada pembuluh darah dan titik lesi kecil di retina.',
            'summary': 'Grad-CAM menyorot pola bercak, perubahan pembuluh, dan area kontras yang mendukung prediksi retinopati diabetik.',
            'reason': 'Model memberi bobot pada indikasi mikroaneurisma, eksudat, atau tekstur tidak normal yang sering muncul pada retinopati diabetik.',
        },
        'normal': {
            'focus': 'Heatmap mengikuti struktur retina yang stabil seperti optic disc dan pembuluh utama.',
            'summary': 'Tidak ada area abnormal dominan yang kuat, sehingga model lebih condong pada prediksi normal.',
            'reason': 'Model membaca sebaran warna, pola pembuluh, dan tekstur retina yang relatif konsisten sebagai sinyal normal.',
        },
    }

    selected = explanations.get(label, {
        'focus': 'Heatmap menunjukkan area citra yang paling memengaruhi keputusan model.',
        'summary': 'Model belum memiliki pola penjelasan spesifik untuk label ini, sehingga interpretasi ditampilkan secara umum.',
        'reason': 'Area dengan intensitas Grad-CAM lebih tinggi dianggap paling berkontribusi pada hasil prediksi.',
    })

    return {
        'status': f'Model memprediksi {predicted_label} dengan keyakinan {confidence_text}.',
        'focus': selected['focus'],
        'summary': selected['summary'],
        'reason': selected['reason'],
        'note': 'XAI membantu melihat alasan model, tetapi hasil tetap perlu dikonfirmasi dengan pemeriksaan klinis.',
    }


def _build_pipeline_data(filename, uploaded_image, hasil, confidence, gradcam_image, file_id=None):
    confidence_value = round(float(confidence or 0), 2)
    predicted_label = hasil or 'Belum terklasifikasi'
    feature_vector_preview = _build_feature_vector_preview(confidence_value, predicted_label)
    xai_explanation = _build_xai_explanation(predicted_label, confidence_value)
    fallback_scores = [
        {'label': 'Normal', 'value': 8.6},
        {'label': 'Cataract', 'value': 5.4},
        {'label': 'Glaucoma', 'value': 3.2},
        {'label': 'Diabetic Retinopathy', 'value': 2.1},
    ]

    # Map English and Indonesian disease names to a canonical form to avoid duplicates.
    label_canonical_map = {
        'cataract': 'cataract',
        'katarak': 'cataract',
        'glaucoma': 'glaucoma',
        'glaukoma': 'glaucoma',
        'diabetic retinopathy': 'diabetic retinopathy',
        'normal': 'normal',
    }

    def _get_canonical(s):
        return label_canonical_map.get((s or '').lower().strip(), (s or '').lower().strip())

    classification_scores = [{'label': predicted_label, 'value': confidence_value}]
    seen = {_get_canonical(predicted_label)}

    for score in fallback_scores:
        canonical = _get_canonical(score.get('label'))
        if canonical in seen:
            continue
        seen.add(canonical)
        classification_scores.append(score)

    return {
        'file_id': file_id,
        'file_name': filename,
        'uploaded_image': uploaded_image,
        'preprocessing': {
            'image': uploaded_image,
            'steps': [
                {'label': 'Resize', 'value': '224 x 224 px'},
                {'label': 'Normalization', 'value': 'Pixel range 0 - 1'},
                {'label': 'Enhancement', 'value': 'Contrast balanced'},
            ],
        },
        'augmentation': {
            'image': uploaded_image,
            'steps': [
                {'label': 'Flip', 'value': 'Horizontal'},
                {'label': 'Rotate', 'value': '+/- 15 derajat'},
                {'label': 'Zoom', 'value': 'Random crop'},
            ],
            'variants': [
                {
                    'label': 'Flip',
                    'icon': 'fa-solid fa-arrows-left-right',
                    'class_name': 'augmentation-flip',
                },
                {
                    'label': 'Rotate',
                    'icon': 'fa-solid fa-rotate-right',
                    'class_name': 'augmentation-rotate',
                },
                {
                    'label': 'Zoom',
                    'icon': 'fa-solid fa-magnifying-glass-plus',
                    'class_name': 'augmentation-zoom',
                },
            ],
        },
        'feature_extraction': {
            'model': 'MobileNetV2',
            'backbone': 'CNN Backbone',
            'input_shape': '224 x 224 x 3',
            'feature_vector': '1280 Features',
            'processing_time': '0.21 sec',
            'layer_focus': 'Deep retinal texture, vessel pattern, optic disc region',
            'vector_preview': feature_vector_preview,
            'processes': [
                {
                    'label': 'Feature Map Terakhir',
                    'value': '7 x 7 x 1280',
                    'icon': 'fa-solid fa-layer-group',
                    'detail': 'Layer akhir MobileNetV2 menghasilkan 1280 channel fitur, masing-masing berukuran 7 x 7.',
                },
                {
                    'label': 'Global Average Pooling',
                    'value': 'v_k = rata-rata F_k',
                    'icon': 'fa-solid fa-calculator',
                    'detail': 'Setiap channel 7 x 7 dirata-ratakan menjadi 1 angka fitur.',
                },
                {
                    'label': 'Hasil 1280 Fitur',
                    'value': '1280 channel x 1 angka',
                    'icon': 'fa-solid fa-vector-square',
                    'detail': 'Karena ada 1280 channel, output akhirnya menjadi vektor berisi 1280 angka.',
                },
            ],
        },
        'classification': {
            'label': predicted_label,
            'confidence': confidence_value,
            'scores': classification_scores[:4],
            'summary': 'Dummy class probability untuk memperlihatkan keluaran klasifikasi model.',
        },
        'gradcam': {
            'image': gradcam_image,
            'summary': xai_explanation['summary'],
        },
        'explanation': {
            'status': xai_explanation['status'],
            'focus': xai_explanation['focus'],
            'reason': xai_explanation['reason'],
            'note': xai_explanation['note'],
        },
    }


@login_required(login_url='/login/')
def deteksi(request):

    print("METHOD:", request.method)

    hasil = None
    confidence = None
    filename = None
    uploaded_image = None
    gradcam_image = None
    pipeline_data = None

    if request.method == "POST":

        print("POST MASUK")

        retina_image = request.FILES.get("retina_image")

        print("FILE:", retina_image)

        if retina_image:

            fs = FileSystemStorage()

            filename = fs.save(
                retina_image.name,
                retina_image
            )

            filepath = fs.path(filename)
            uploaded_image = fs.url(filename)

            print("FILEPATH:", filepath)

            hasil, confidence = predict_image(filepath)

            print("HASIL:", hasil)
            print("CONFIDENCE:", confidence)

            gradcam_filename = "gradcam_" + filename

            record_id = None
            if request.user.is_authenticated:
                history = DetectionHistory.objects.create(
                    user=request.user,
                    image=filename,
                    result=hasil,
                    confidence=confidence,
                    gradcam_image=gradcam_filename
                )
                record_id = history.pk

            gradcam_path = fs.path(gradcam_filename)

            try:
                generate_gradcam(filepath, gradcam_path)
                gradcam_image = fs.url(gradcam_filename)
            except Exception as exc:
                logger.exception('Gagal menghasilkan Grad-CAM untuk %s.', filepath)
                gradcam_image = None
                messages.warning(request, f'Prediksi berhasil, tetapi visualisasi Grad-CAM tidak dapat dibuat: {exc}')

            # derive a display id: prefer DB record id
            display_id = record_id

            # If no DB id, try to locate the image in the dataset folders to get class and index
            if not display_id and filename:
                dataset_root = getattr(settings, 'DATASET_ROOT', None)
                found = False
                if dataset_root:
                    try:
                        # search train and test subfolders and dataset root
                        search_paths = [dataset_root, dataset_root / 'train', dataset_root / 'test']
                        for sp in search_paths:
                            if not sp or not sp.exists():
                                continue
                            for class_dir in sp.iterdir():
                                if not class_dir.is_dir():
                                    continue
                                # get sorted list of image files in the class folder
                                images = sorted([p for p in class_dir.iterdir() if p.suffix.lower() in DATASET_IMAGE_EXTENSIONS])
                                target_name = Path(filename).name.lower()
                                for idx, img in enumerate(images, start=1):
                                    img_name = img.name.lower()
                                    if img_name == filename.lower() or img_name == target_name or target_name in img_name or img_name in target_name:
                                        display_id = f"{class_dir.name} #{idx}"
                                        found = True
                                        break
                                if found:
                                    break
                            if found:
                                break
                    except Exception:
                        # ignore dataset search errors and fall back
                        found = False

                # if still not found, prefer the original uploaded name (without suffix),
                # otherwise try extract numeric id from filename or fallback to stem
                if not found:
                    original_name = getattr(retina_image, 'name', None)
                    if original_name:
                        try:
                            display_id = Path(original_name).stem
                        except Exception:
                            display_id = original_name
                    else:
                        m = re.search(r"(\d+)", filename)
                        if m:
                            display_id = m.group(1)
                        else:
                            try:
                                display_id = Path(filename).stem
                            except Exception:
                                display_id = filename

            pipeline_data = _build_pipeline_data(
                filename,
                uploaded_image,
                hasil,
                confidence,
                gradcam_image,
                file_id=display_id
            )

            print("HASIL:", hasil)
            print("CONFIDENCE:", confidence)

    return render(
    request,
    "deteksi.html",
    {
        "hasil": hasil,
        "confidence": confidence,
        "filename": filename,
        "uploaded_image": uploaded_image,
        "gradcam_image": gradcam_image,
        "pipeline_data": pipeline_data,
    }
)

def cara_kerja(request):
    return redirect('home')

@login_required(login_url='/login/')
def profile(request):
    total_screenings = 0
    last_screening = None
    profile_image_url = None
    profile = None

    if request.user.is_authenticated:
        total_screenings = DetectionHistory.objects.filter(user=request.user).count()
        last_screening = DetectionHistory.objects.filter(user=request.user).order_by('-created_at').first()
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.image:
            profile_image_url = profile.image.url

    if request.method == 'POST' and request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        uploaded_image = request.FILES.get('profile_image')
        if uploaded_image:
            profile.image = uploaded_image
            profile.save()
            messages.success(request, 'Foto profil berhasil diperbarui.')
            return redirect('profile')
        else:
            messages.warning(request, 'Tidak ada file yang dipilih.')

    return render(request, 'profile.html', {
        'total_screenings': total_screenings,
        'last_screening': last_screening,
        'profile_image_url': profile_image_url,
    })

@login_required(login_url='/login/')
def riwayat(request):
    screenings = []
    total_screenings = 0
    average_confidence = 0
    last_screening = None
    profile = None

    if request.user.is_authenticated:
        screenings = DetectionHistory.objects.filter(user=request.user).order_by('-created_at')
        total_screenings = screenings.count()
        average_confidence = screenings.aggregate(avg=Avg('confidence'))['avg'] or 0
        last_screening = screenings.first()
        try:
            profile = request.user.profile
        except Exception:
            pass

    return render(request, 'riwayat-skrining.html', {
        'screenings': screenings,
        'total_screenings': total_screenings,
        'average_confidence': average_confidence,
        'last_screening': last_screening,
        'profile': profile,
    })

@login_required(login_url='/login/')
def faq(request):
    faq_sections = [
        {
            'title': 'KEAMANAN & PRIVASI',
            'items': [
                {
                    'q': 'Bagaimana terkait keamanan dan kerahasiaan data pengguna EyeDetect.com?',
                    'a': "Kami memahami bahwa data citra mata dan informasi kesehatan bersifat sensitif. Secara umum, praktik yang diterapkan platform skrining kesehatan seperti ini meliputi:<ul><li>Enkripsi data saat pengiriman maupun penyimpanan</li><li>Akses data dibatasi hanya untuk kebutuhan analisis dan ditangani oleh pihak yang berwenang</li><li>Data tidak dibagikan ke pihak ketiga tanpa persetujuan pengguna</li><li>Pengguna dapat meminta penghapusan data sesuai kebijakan privasi yang berlaku</li></ul>"
                }
            ]
        },
        {
            'title': 'CARA KERJA',
            'items': [
                {
                    'q': 'Bagaimana cara kerja skrining EyeDetect?',
                    'a': "Skrining EyeDetect bekerja dengan langkah berikut:<ol><li>Pengguna mengunggah citra retina/mata.</li><li>Sistem memproses citra menggunakan model deep learning (CNN berbasis MobileNetV2) yang telah dilatih mengenali pola-pola indikasi penyakit mata.</li><li>Model menganalisis citra dan menghasilkan prediksi beserta tingkat kepercayaan (confidence score).</li><li>Hasil dilengkapi visualisasi Explainable AI (XAI) yang menunjukkan area citra mana yang paling memengaruhi hasil prediksi, sehingga proses analisis lebih transparan.</li></ol>"
                }
            ]
        },
        {
            'title': 'HASIL SKRINING',
            'items': [
                {
                    'q': 'Bagaimana hasil dari skrining EyeDetect?',
                    'a': "Hasil skrining biasanya ditampilkan dalam bentuk:<ul><li><strong>Kategori/indikasi</strong> kondisi mata yang terdeteksi (misalnya normal atau indikasi kondisi tertentu)</li><li><strong>Tingkat kepercayaan (confidence score)</strong> dari prediksi tersebut</li><li><strong>Visualisasi XAI</strong> yang menyorot area citra sebagai dasar keputusan model</li></ul>"
                }
            ]
        },
        {
            'title': 'AKURASI',
            'items': [
                {
                    'q': 'Seberapa jauh keakuratannya?',
                    'a': "Tingkat akurasi model bergantung pada kualitas dan keragaman data yang digunakan saat pelatihan, serta kualitas citra yang diunggah pengguna (pencahayaan, fokus, sudut pengambilan). Seperti sistem skrining berbasis AI pada umumnya, EyeDetect <strong>tidak memiliki akurasi 100%</strong> dan dapat menghasilkan false positive (salah mendeteksi ada kelainan) maupun false negative (gagal mendeteksi kelainan yang sebenarnya ada). Oleh karena itu, hasil skrining tidak menggantikan pemeriksaan klinis oleh dokter mata."
                }
            ]
        },
        {
            'title': 'TEKNIS',
            'items': [
                {
                    'q': 'Apa yang terjadi jika saya hanya menebak dengan benar?',
                    'a': 'EyeDetect bukan merupakan tes berbasis tebakan pengguna — sistem ini bekerja dengan menganalisis citra mata Anda secara otomatis menggunakan model AI, bukan berdasarkan jawaban atau tebakan yang Anda masukkan. Jadi, hasil skrining murni berasal dari analisis citra, bukan dari sesi tanya-jawab yang bisa "ditebak".'
                }
            ]
        },
        {
            'title': 'MENGAPA HARUS PERIKSA',
            'items': [
                {
                    'q': 'Mengapa saya harus memeriksakan penglihatan saya?',
                    'a': 'Banyak gangguan mata seperti glaukoma, retinopati diabetik, dan katarak tidak menunjukkan gejala yang jelas pada tahap awal. Pemeriksaan rutin membantu mendeteksi kelainan sejak dini sebelum menyebabkan kerusakan permanen atau kehilangan penglihatan, sehingga penanganan dapat dilakukan lebih cepat dan efektif.'
                }
            ]
        },
        {
            'title': 'RISIKO',
            'items': [
                {
                    'q': 'Siapa yang berisiko mengalami gangguan penglihatan?',
                    'a': 'Beberapa kelompok yang memiliki risiko lebih tinggi antara lain:<ul><li>Penderita diabetes (berisiko retinopati diabetik)</li><li>Orang dengan riwayat keluarga penyakit mata (misalnya glaukoma)</li><li>Lansia (risiko katarak dan degenerasi makula meningkat seiring usia)</li><li>Orang dengan tekanan darah tinggi atau kondisi kardiovaskular tertentu</li><li>Orang yang sering terpapar sinar UV tanpa pelindung mata</li><li>Perokok aktif</li></ul>'
                }
            ]
        },
        {
            'title': 'TEMPAT TES',
            'items': [
                {
                    'q': 'Saya tidak tahu di mana saya bisa menjalani tes penglihatan. Apa yang harus saya lakukan?',
                    'a': 'Anda bisa memeriksakan penglihatan di:<ul><li>Klinik mata atau rumah sakit terdekat dengan layanan spesialis mata (dokter spesialis mata/SpM)</li><li>Optik yang menyediakan layanan pemeriksaan refraksi dasar</li><li>Puskesmas yang memiliki layanan kesehatan mata</li></ul>'
                }
            ]
        }
    ]

    return render(request, 'faq.html', {
        'faq_sections': faq_sections,
    })


def _build_dataset_context(request, dataset_template, current_page='dataset'):
    if request.method == 'POST':
        dataset_file = request.FILES.get('dataset_file')
        disease = request.POST.get('disease', '').strip()

        if not dataset_file or not disease:
            messages.error(request, 'Unggah file gambar dan pilih kelas penyakit.')
        else:
            try:
                dataset_sample = DatasetSample.objects.create(
                    source_file=dataset_file,
                    label=disease,
                )
                try:
                    from ai_model.feature_extractor import extract_feature_pattern
                    pattern = extract_feature_pattern(dataset_sample.source_file.path)
                    dataset_sample.pattern = pattern
                    dataset_sample.save(update_fields=['pattern'])
                except Exception:
                    logger.exception('Gagal ekstraksi fitur untuk dataset baru.')
                    messages.warning(request, 'Dataset berhasil disimpan, tetapi pola fitur belum dapat diekstrak.')

                messages.success(request, 'Dataset berhasil diunggah dan disimpan ke database.')
            except Exception:
                logger.exception('Gagal menyimpan dataset baru.')
                messages.error(request, 'Terjadi kesalahan saat menyimpan dataset. Coba lagi.')

    search_query = request.GET.get('search', '').strip()
    dataset_qs = DatasetSample.objects.all().order_by('-created_at')

    if search_query:
        dataset_qs = dataset_qs.filter(
            Q(label__icontains=search_query) |
            Q(source_file__icontains=search_query)
        )

    total_items = dataset_qs.count()
    page = max(1, int(request.GET.get('page', 1)))
    page_size = 6
    total_pages = max(1, math.ceil(total_items / page_size))
    if page > total_pages:
        page = total_pages
    start = (page - 1) * page_size
    end = start + page_size

    dataset_samples = dataset_qs[start:end]
    dataset_items = []
    for sample in dataset_samples:
        pattern = sample.pattern or []
        snippet = ', '.join(f'{value:.2f}' for value in pattern[:8])
        if len(pattern) > 8:
            snippet += ', ...'

        dataset_items.append({
            'id': f'DS-{sample.pk}',
            'label': sample.label,
            'upload_date': sample.created_at.strftime('%d %B %Y'),
            'size': f"{round(sample.source_file.size / 1024)} KB" if sample.source_file else 'N/A',
            'status': 'Tersimpan',
            'pattern_snippet': snippet or 'Belum diekstrak',
            'pattern_count': len(pattern),
        })

    return {
        'dataset_items': dataset_items,
        'dataset_page': page,
        'dataset_total_pages': total_pages,
        'search_query': search_query,
        'current_page': current_page,
    }


def _get_admin_data():
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    new_users_last_week = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7)).count()
    total_predictions = DetectionHistory.objects.count()

    try:
        total_dataset = DatasetSample.objects.count()
    except Exception:
        dataset_dir = os.path.join(settings.MEDIA_ROOT, 'dataset_uploads')
        total_dataset = 0
        if os.path.isdir(dataset_dir):
            total_dataset = sum(
                1 for item in os.listdir(dataset_dir)
                if os.path.isfile(os.path.join(dataset_dir, item))
            )

    stats = {
        'total_dataset': total_dataset,
        'total_predictions': total_predictions,
        'model_accuracy': '89.32%',
        'total_users': total_users,
        'active_users': active_users,
        'new_users_last_week': new_users_last_week,
    }

    latest_predictions_qs = DetectionHistory.objects.select_related('user').order_by('-created_at')[:5]
    latest_predictions = []
    for detection in latest_predictions_qs:
        latest_predictions.append({
            'id': f'PRD-{detection.pk}',
            'result': detection.result,
            'confidence': round(detection.confidence, 2),
            'user': detection.user.username,
            'date': detection.created_at.strftime('%d %B %Y %H:%M'),
            'image_url': detection.image.url if detection.image else None,
        })

    dataset_items = [
        {'id': 'DS-1245', 'image': 'https://images.unsplash.com/photo-1580281657528-843557120a72?auto=format&fit=crop&w=80&q=80', 'disease': 'Glaukoma', 'upload_date': '20 Mei 2026', 'size': '256 KB', 'status': 'Verified'},
        {'id': 'DS-1244', 'image': 'https://images.unsplash.com/photo-1515942401378-4847d02f31f3?auto=format&fit=crop&w=80&q=80', 'disease': 'Diabetic Retinopathy', 'upload_date': '20 Mei 2026', 'size': '312 KB', 'status': 'Verified'},
        {'id': 'DS-1243', 'image': 'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=80&q=80', 'disease': 'Katarak', 'upload_date': '19 Mei 2026', 'size': '245 KB', 'status': 'Pending'},
        {'id': 'DS-1242', 'image': 'https://images.unsplash.com/photo-1485217988980-11786ced9454?auto=format&fit=crop&w=80&q=80', 'disease': 'Normal', 'upload_date': '19 Mei 2026', 'size': '198 KB', 'status': 'Verified'},
        {'id': 'DS-1241', 'image': 'https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?auto=format&fit=crop&w=80&q=80', 'disease': 'Glaukoma', 'upload_date': '18 Mei 2026', 'size': '276 KB', 'status': 'Reviewed'},
        {'id': 'DS-1240', 'image': 'https://images.unsplash.com/photo-1495433324511-bf8e92934d90?auto=format&fit=crop&w=80&q=80', 'disease': 'Normal', 'upload_date': '18 Mei 2026', 'size': '212 KB', 'status': 'Verified'},
      ]

    model_info = {
        'name': 'RetinaNet Premium AI',
        'version': 'v3.1',
        'accuracy': '89.32%',
        'precision': '91.8%',
        'recall': '87.4%',
        'trained_at': '20 Mei 2026',
        'architecture': 'ResNet50 + DenseNet',
        'parameters': '24.8M',
        'status': 'Production',
    }

    model_history = [
        {'version': 'v3.1', 'accuracy': '89.32%', 'date': '20 Mei 2026', 'status': 'Production'},
        {'version': 'v3.0', 'accuracy': '88.01%', 'date': '15 Mei 2026', 'status': 'Staging'},
        {'version': 'v2.8', 'accuracy': '85.43%', 'date': '10 Mei 2026', 'status': 'Archive'},
      ]

    prediction_distribution = {
        'labels': ['Normal', 'Katarak', 'Glaukoma', 'Diabetic Retinopathy'],
        'values': [35, 21, 27, 17],
      }

    monthly_trend = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei'],
        'values': [320, 420, 380, 460, 520],
    }

    activity_logs = [
        {'time': '20 Mei 2026 14:35', 'action': 'User login', 'user': 'user123', 'status': 'Berhasil'},
        {'time': '20 Mei 2026 14:20', 'action': 'Prediksi baru dibuat', 'user': 'user456', 'status': 'Berhasil'},
        {'time': '20 Mei 2026 13:50', 'action': 'Dataset ditambahkan', 'user': 'admin', 'status': 'Berhasil'},
    ]

    users_list = list(User.objects.all().order_by('-date_joined'))

    return {
        'stats': stats,
        'latest_predictions': latest_predictions,
        'dataset_items': dataset_items,
        'model_info': model_info,
        'model_history': model_history,
        'prediction_distribution': prediction_distribution,
        'monthly_trend': monthly_trend,
        'activity_logs': activity_logs,
        'users_list': users_list,
    }


@staff_required
def admin_dashboard(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Dashboard',
        'current_page': 'dashboard',
    })
    return render(request, 'admin_dashboard.html', context)


@staff_required
def admin_dataset(request):
    active_split = request.GET.get('split', 'train').lower()
    if active_split not in DATASET_SPLITS:
        active_split = 'train'

    search_query = request.GET.get('q', '').strip()
    dataset = scan_dataset()
    visible_classes = dataset[active_split]['classes']
    if search_query:
        normalized_query = search_query.casefold()
        visible_classes = [
            item for item in visible_classes
            if normalized_query in item['name'].casefold()
            or normalized_query in item['slug'].casefold()
        ]

    combined_distribution = []
    grand_total = dataset['train']['total'] + dataset['test']['total']
    for index, class_meta in enumerate(DATASET_CLASSES):
        class_total = (
            dataset['train']['classes'][index]['count']
            + dataset['test']['classes'][index]['count']
        )
        combined_distribution.append({
            'name': class_meta['name'],
            'theme': class_meta['theme'],
            'count': class_total,
            'percentage': round(class_total / grand_total * 100, 1) if grand_total else 0,
        })

    context = {
        'page_title': 'Dataset Retina',
        'current_page': 'dataset',
        'active_split': active_split,
        'active_split_label': active_split.title(),
        'classes': visible_classes,
        'class_count': len(DATASET_CLASSES),
        'train_total': dataset['train']['total'],
        'test_total': dataset['test']['total'],
        'grand_total': grand_total,
        'combined_distribution': combined_distribution,
        'chart_data': {
            'labels': [item['name'] for item in dataset[active_split]['classes']],
            'values': [item['count'] for item in dataset[active_split]['classes']],
        },
        'search_query': search_query,
        'scanned_at': datetime.now().strftime('%d %b %Y, %H:%M'),
    }
    return render(request, 'admin_dataset.html', context)


@staff_required
def admin_dataset_detail(request, split, class_slug):
    if split not in DATASET_SPLITS or class_slug not in DATASET_CLASS_MAP:
        raise Http404('Kelas dataset tidak ditemukan.')

    class_meta = DATASET_CLASS_MAP[class_slug]
    search_query = request.GET.get('q', '').strip()
    filenames = list_dataset_images(split, class_slug)
    total_unfiltered = len(filenames)
    if search_query:
        normalized_query = search_query.casefold()
        filenames = [name for name in filenames if normalized_query in name.casefold()]

    paginator = Paginator(filenames, 24)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    start_index = page_obj.start_index() if paginator.count else 0
    images = [
        {
            'name': filename,
            'url': dataset_image_url(split, class_slug, filename),
            'number': start_index + index,
        }
        for index, filename in enumerate(page_obj.object_list)
    ]

    context = {
        'page_title': f"{class_meta['name']} - {split.title()}",
        'current_page': 'dataset',
        'split': split,
        'split_label': split.title(),
        'other_split': 'test' if split == 'train' else 'train',
        'class_meta': class_meta,
        'images': images,
        'image_total': total_unfiltered,
        'filtered_total': paginator.count,
        'search_query': search_query,
        'page_obj': page_obj,
        'page_range': [
            item if isinstance(item, int) else None
            for item in paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
        ],
    }
    return render(request, 'admin_dataset_detail.html', context)


@staff_required
def admin_dataset_image(request, split, class_slug, filename):
    directory = dataset_directory(split, class_slug).resolve()
    candidate = (directory / filename).resolve()

    if (
        candidate.parent != directory
        or candidate.suffix.lower() not in DATASET_IMAGE_EXTENSIONS
        or not candidate.is_file()
    ):
        raise Http404('Gambar dataset tidak ditemukan.')

    content_type = mimetypes.guess_type(candidate.name)[0] or 'application/octet-stream'
    response = FileResponse(candidate.open('rb'), content_type=content_type)
    response['Cache-Control'] = 'private, max-age=3600'
    return response


def user_dataset(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = _build_dataset_context(request, 'user_dataset.html', current_page='dataset')
    return render(request, 'user_dataset.html', context)


@staff_required
def admin_predictions(request):
    context = _get_admin_data()

    detections = DetectionHistory.objects.select_related('user').order_by('-created_at')
    latest_predictions = []
    for detection in detections[:5]:
        latest_predictions.append({
            'id': f'PRD-{detection.pk}',
            'result': detection.result,
            'confidence': round(detection.confidence, 2),
            'user': detection.user.username,
            'date': detection.created_at.strftime('%d %B %Y %H:%M'),
            'image_url': detection.image.url if detection.image else None,
        })

    distribution_qs = detections.values('result').annotate(count=Count('id')).order_by('-count')
    if distribution_qs:
        distribution_labels = [item['result'] for item in distribution_qs]
        distribution_values = [item['count'] for item in distribution_qs]
    else:
        distribution_labels = ['Normal', 'Katarak', 'Glaukoma', 'Diabetic Retinopathy']
        distribution_values = [0, 0, 0, 0]

    context.update({
        'page_title': 'Hasil Prediksi',
        'current_page': 'predictions',
        'latest_predictions': latest_predictions,
        'prediction_distribution': {
            'labels': distribution_labels,
            'values': distribution_values,
        },
    })
    return render(request, 'admin_predictions.html', context)


@staff_required
def admin_model_cnn(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Model CNN',
        'current_page': 'model',
    })
    return render(request, 'admin_model_cnn.html', context)


@staff_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')

    return render(
        request,
        'admin_users.html',
        {
            'page_title': 'Pengguna',
            'current_page': 'users',
            'users': users,
            'total_users': users.count()
        }
    )


@staff_required
def admin_settings(request):
    context = _get_admin_data()
    context.update({
        'page_title': 'Pengaturan',
        'current_page': 'settings',
        'settings': {
            'app_name': 'EyeDetect',
            'admin_email': 'admin@example.com',
            'system_mode': 'Online',
            'email_notifications': True,
            'two_factor_auth': False,
            'maintenance_mode': False,
        },
    })
    return render(request, 'admin_settings.html', context)


@staff_required
def admin_activity(request):
    context = _get_admin_data()
    context.update({'page_title': 'Riwayat Aktivitas', 'current_page': 'activity'})
    return render(request, 'admin_activity.html', context)

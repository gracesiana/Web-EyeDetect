import logging
import os
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.urls import reverse

logger = logging.getLogger(__name__)

DATASET_SPLITS = ('train', 'test')
DATASET_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
DATASET_CLASSES = (
    {
        'slug': 'diabetic_retinopathy',
        'name': 'Diabetic Retinopathy',
        'description': 'Citra retina dengan indikasi kerusakan pembuluh darah akibat diabetes.',
        'theme': 'retinopathy',
    },
    {
        'slug': 'cataract',
        'name': 'Cataract',
        'description': 'Citra mata dengan karakteristik kekeruhan pada lensa.',
        'theme': 'cataract',
    },
    {
        'slug': 'glaucoma',
        'name': 'Glaucoma',
        'description': 'Citra retina dengan karakteristik kerusakan saraf optik.',
        'theme': 'glaucoma',
    },
    {
        'slug': 'normal',
        'name': 'Normal',
        'description': 'Citra retina sehat tanpa indikasi penyakit yang terdeteksi.',
        'theme': 'normal',
    },
)
DATASET_CLASS_MAP = {item['slug']: item for item in DATASET_CLASSES}


def dataset_root():
    configured_root = getattr(
        settings,
        'DATASET_ROOT',
        Path(settings.BASE_DIR) / 'EyeDetect' / 'dataset',
    )
    return Path(configured_root)


def dataset_directory(split, class_slug):
    if split not in DATASET_SPLITS or class_slug not in DATASET_CLASS_MAP:
        raise Http404('Folder dataset tidak ditemukan.')
    return dataset_root() / split / class_slug


def list_dataset_images(split, class_slug):
    directory = dataset_directory(split, class_slug)
    if not directory.is_dir():
        return []

    try:
        filenames = os.listdir(directory)
    except OSError:
        logger.exception('Gagal membaca folder dataset %s.', directory)
        return []

    return sorted(
        filename
        for filename in filenames
        if (directory / filename).is_file()
        and Path(filename).suffix.lower() in DATASET_IMAGE_EXTENSIONS
    )


def dataset_image_url(split, class_slug, filename):
    return reverse(
        'admin_panel_dataset_image',
        kwargs={
            'split': split,
            'class_slug': class_slug,
            'filename': filename,
        },
    )


def scan_dataset():
    scan = {}
    for split in DATASET_SPLITS:
        classes = []
        for class_meta in DATASET_CLASSES:
            filenames = list_dataset_images(split, class_meta['slug'])
            classes.append({
                **class_meta,
                'count': len(filenames),
                'thumbnail_url': (
                    dataset_image_url(split, class_meta['slug'], filenames[0])
                    if filenames else None
                ),
            })

        total = sum(item['count'] for item in classes)
        for item in classes:
            item['percentage'] = round((item['count'] / total * 100), 1) if total else 0
        scan[split] = {'classes': classes, 'total': total}
    return scan

import tempfile
from pathlib import Path

from django.test import SimpleTestCase, override_settings
from django.urls import reverse


class AdminDatasetViewsTests(SimpleTestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.dataset_root = Path(self.temp_directory.name)
        self.settings_override = override_settings(DATASET_ROOT=self.dataset_root)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

        for split in ('train', 'test'):
            for class_slug in ('diabetic_retinopathy', 'cataract', 'glaucoma', 'normal'):
                directory = self.dataset_root / split / class_slug
                directory.mkdir(parents=True)
                (directory / 'preview.jpg').write_bytes(b'fake-image')

        cataract_train = self.dataset_root / 'train' / 'cataract'
        for number in range(1, 30):
            (cataract_train / f'image-{number:02}.png').write_bytes(b'png-image')
        (cataract_train / 'ignore.txt').write_text('not an image', encoding='utf-8')

    def test_overview_reads_counts_from_dataset_folders(self):
        response = self.client.get(reverse('admin_panel_dataset'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['train_total'], 33)
        self.assertEqual(response.context['test_total'], 4)
        self.assertEqual(len(response.context['classes']), 4)
        self.assertContains(response, 'Diabetic Retinopathy')

    def test_overview_supports_split_and_class_search(self):
        response = self.client.get(
            reverse('admin_panel_dataset'),
            {'split': 'test', 'q': 'glaucoma'},
        )

        self.assertEqual(response.context['active_split'], 'test')
        self.assertEqual([item['slug'] for item in response.context['classes']], ['glaucoma'])

    def test_detail_paginates_images_and_filters_by_filename(self):
        detail_url = reverse(
            'admin_panel_dataset_detail',
            kwargs={'split': 'train', 'class_slug': 'cataract'},
        )

        second_page = self.client.get(detail_url, {'page': 2})
        filtered = self.client.get(detail_url, {'q': 'image-01'})

        self.assertEqual(second_page.status_code, 200)
        self.assertEqual(second_page.context['image_total'], 30)
        self.assertEqual(second_page.context['page_obj'].paginator.num_pages, 2)
        self.assertEqual(len(second_page.context['images']), 6)
        self.assertEqual(filtered.context['filtered_total'], 1)

    def test_image_endpoint_streams_only_valid_dataset_images(self):
        image_url = reverse(
            'admin_panel_dataset_image',
            kwargs={
                'split': 'train',
                'class_slug': 'normal',
                'filename': 'preview.jpg',
            },
        )
        response = self.client.get(image_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')
        self.assertEqual(b''.join(response.streaming_content), b'fake-image')

        invalid_url = reverse(
            'admin_panel_dataset_detail',
            kwargs={'split': 'train', 'class_slug': 'unknown'},
        )
        self.assertEqual(self.client.get(invalid_url).status_code, 404)

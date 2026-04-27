import os
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Подгружает в БД информации о месте из JSON файла по URL.'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url', type=str, help='URL json файла с данными о месте.'
        )

    def handle(self, *args, **options):
        json_url = options['json_url']

        response = requests.get(json_url)
        response.raise_for_status()
        payload = response.json()

        title = payload.get('title')
        description_short = payload.get('description_short', '')
        description_long = payload.get('description_long', '')
        longitude = payload['coordinates'].get('lng')
        latitude = payload['coordinates'].get('lat')
        image_urls = payload.get('imgs', [])

        place, created = Place.objects.get_or_create(
            title=title,
            defaults={
                'description_short': description_short,
                'description_long': description_long,
                'longitude': longitude,
                'latitude': latitude,
            },
        )

        if image_urls:
            self.download_images(place, image_urls)

        if created:
            self.stdout.write(f'Место было удачно записано - {title}')

    def download_images(self, place, image_urls):
        for index, image_url in enumerate(image_urls):
            try:
                response = requests.get(
                    image_url,
                )
                response.raise_for_status()

                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path)

                place_image = PlaceImage(place=place, order=index + 1)

                place_image.image.save(
                    filename, ContentFile(response.content), save=True
                )
            except Exception as e:
                self.stdout.write(
                    f'Произошла ошибка при загрузке фото {image_url}\n'
                    f'Ошибка: {e}'
                )

import json
import os
from urllib.parse import urlparse
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place, PlaceImage

import requests



class Command(BaseCommand):
    help = 'Подгружает в БД информации о местах из JSON файлов.'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_directory',
            type=str,
            help='Путь к директории c json файлами'
        )

    def handle(self, *args, **options):
        json_directory = Path(options['json_directory'])
        json_files = list(json_directory.glob('*.json'))
        
        if not json_files:
            self.stdout.write(self.style.WARNING(
                'В указанной директории не обнаружено json файлов'
            ))
            
        files_found = len(json_files)
        object_created = 0
        error_creation = 0
        
        for json_file in json_files:
            result = self.processing_file(json_file)
            if result == 'success':
                object_created += 1
            elif result == 'error':
                error_creation += 1
                
        self.stdout.write(
            f'Найдено файлов: {files_found}\n'
            f'Создано новых мест: {object_created}\n'
            f'Ошибок при создании: {error_creation}'
        )

    def processing_file(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            title = data.get('title')
            description_short = data.get('description_short')
            description_long = data.get('description_long')
            longitude = data['coordinates'].get('lng')
            latitude = data['coordinates'].get('lat')
            image_urls = data.get('imgs', [])
            
            place, created = Place.objects.get_or_create(
                title=title,
                defaults= {
                    'description_short': description_short,
                    'description_long': description_long,
                    'longitude':longitude,
                    'latitude': latitude,
                }
            )
            
            if image_urls:
                self.download_images(place, image_urls)
            
            if created:
                return 'success'

        except Exception as e:
            self.stdout.write(f'При загрузке нового места произошла ошибка: {e}')
            return 'error'
        
    def download_images(self, place, image_urls):
        for order, image_url in enumerate(image_urls):
            try:
                response = requests.get(image_url, )
                response.raise_for_status()
                
                parsed_url = urlparse(image_url)
                filename = os.path.basename(parsed_url.path)
                
                place_image = PlaceImage(
                    place = place,
                    order = order + 1
                )
                
                place_image.image.save(
                    filename,
                    ContentFile(response.content),
                    save=True
                )
            except Exception as e:
                self.stdout.write(
                    f'Произошла ошибка при загрузке фото {image_url}\n'
                    f'Ошибка: {e}'
                )
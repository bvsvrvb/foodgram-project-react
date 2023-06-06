import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Добавляет теги в БД из CSV'

    def handle(self, *args, **options):
        file_path = os.path.join(
            settings.BASE_DIR, 'data/', 'tags.csv')

        Tag.objects.all().delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Tag.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2]
                )
            f.close()

        print('Данные успешно загружены')

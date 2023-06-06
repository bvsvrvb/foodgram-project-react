import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Добавляет ингредиенты в БД из CSV'

    def handle(self, *args, **options):
        file_path = os.path.join(
            settings.BASE_DIR, 'data/', 'ingredients.csv')

        Ingredient.objects.all().delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
            f.close()

        print('Данные успешно загружены')

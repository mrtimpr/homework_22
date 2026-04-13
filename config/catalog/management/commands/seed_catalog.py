from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет старые данные и загружает тестовые категории и продукты из фикстур'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        fixtures_dir = Path(__file__).resolve().parents[2] / 'fixtures'

        call_command('loaddata', str(fixtures_dir / 'categories.json'))
        call_command('loaddata', str(fixtures_dir / 'products.json'))

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены'))

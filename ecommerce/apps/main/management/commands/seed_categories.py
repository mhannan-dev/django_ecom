from django.core.management.base import BaseCommand
from apps.main.models import Category

class Command(BaseCommand):
    help = 'Seed the main categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Laptops', 'slug': 'laptops', 'status': 1, 'parent_slug': None},
            {'name': 'Gaming Laptops', 'slug': 'gaming-laptops', 'status': 1, 'parent_slug': 'laptops'},
            {'name': 'Ultrabooks', 'slug': 'ultrabooks', 'status': 1, 'parent_slug': 'laptops'},
            {'name': 'Desktops', 'slug': 'desktops', 'status': 1, 'parent_slug': None},
            {'name': 'Gaming Desktops', 'slug': 'gaming-desktops', 'status': 1, 'parent_slug': 'desktops'},
            {'name': 'Processors', 'slug': 'processors', 'status': 1, 'parent_slug': None},
            {'name': 'Intel Processors', 'slug': 'intel-processors', 'status': 1, 'parent_slug': 'processors'},
            {'name': 'AMD Processors', 'slug': 'amd-processors', 'status': 1, 'parent_slug': None},
            {'name': 'Motherboards', 'slug': 'motherboards', 'status': 1, 'parent_slug': None},
            {'name': 'ATX Motherboards', 'slug': 'atx-motherboards', 'status': 1, 'parent_slug': 'motherboards'},
            {'name': 'Accessories', 'slug': 'accessories', 'status': 1, 'parent_slug': None},
            {'name': 'Laptop Bags', 'slug': 'laptop-bags', 'status': 1, 'parent_slug': 'accessories'},
            {'name': 'Laptop Stands', 'slug': 'laptop-stands', 'status': 1, 'parent_slug': 'accessories'},
        ]

        for category in categories:
            parent_category = Category.objects.filter(slug=category['parent_slug']).first() if category['parent_slug'] else None
            Category.objects.update_or_create(
                slug=category['slug'],
                defaults={
                    'name': category['name'],
                    'status': category['status'],
                    'parent': parent_category
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded categories'))

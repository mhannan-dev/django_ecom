import os
from django.core.management.base import BaseCommand
from apps.main.models import Category, Product
from django.utils.text import slugify
from django.core.files import File

class Command(BaseCommand):
    help = 'Seed the products'

    def handle(self, *args, **kwargs):
        products = [
            # Laptops
            {
                'name': 'Dell XPS 13',
                'category_slug': 'laptops',
                'description': 'A powerful and compact laptop.',
                'image': 'path_to_image/dell_xps_13.jpg',
                'original_price': 999.99,
                'discount_percentage': 10.0,
                'meta_title': 'Dell XPS 13',
                'meta_description': 'A powerful and compact laptop by Dell.',
                'meta_tags': 'dell, xps, laptop',
            },
            {
                'name': 'HP Spectre x360',
                'category_slug': 'laptops',
                'description': 'A versatile and stylish laptop.',
                'image': 'path_to_image/hp_spectre_x360.jpg',
                'original_price': 1099.99,
                'discount_percentage': 12.0,
                'meta_title': 'HP Spectre x360',
                'meta_description': 'A versatile and stylish laptop by HP.',
                'meta_tags': 'hp, spectre, laptop',
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon',
                'category_slug': 'laptops',
                'description': 'A durable and reliable business laptop.',
                'image': 'path_to_image/lenovo_thinkpad_x1_carbon.jpg',
                'original_price': 1299.99,
                'discount_percentage': 8.0,
                'meta_title': 'Lenovo ThinkPad X1 Carbon',
                'meta_description': 'A durable and reliable business laptop by Lenovo.',
                'meta_tags': 'lenovo, thinkpad, laptop',
            },
            # Gaming Laptops
            {
                'name': 'Asus ROG Zephyrus',
                'category_slug': 'gaming-laptops',
                'description': 'A high-performance gaming laptop.',
                'image': 'path_to_image/asus_rog_zephyrus.jpg',
                'original_price': 1499.99,
                'discount_percentage': 15.0,
                'meta_title': 'Asus ROG Zephyrus',
                'meta_description': 'A high-performance gaming laptop by Asus.',
                'meta_tags': 'asus, rog, gaming, laptop',
            },
            {
                'name': 'MSI GS66 Stealth',
                'category_slug': 'gaming-laptops',
                'description': 'A sleek and powerful gaming laptop.',
                'image': 'path_to_image/msi_gs66_stealth.jpg',
                'original_price': 1599.99,
                'discount_percentage': 14.0,
                'meta_title': 'MSI GS66 Stealth',
                'meta_description': 'A sleek and powerful gaming laptop by MSI.',
                'meta_tags': 'msi, gs66, gaming, laptop',
            },
            {
                'name': 'Acer Predator Helios 300',
                'category_slug': 'gaming-laptops',
                'description': 'A budget-friendly gaming laptop.',
                'image': 'path_to_image/acer_predator_helios_300.jpg',
                'original_price': 1299.99,
                'discount_percentage': 13.0,
                'meta_title': 'Acer Predator Helios 300',
                'meta_description': 'A budget-friendly gaming laptop by Acer.',
                'meta_tags': 'acer, predator, gaming, laptop',
            },
            # Ultrabooks
            {
                'name': 'MacBook Air',
                'category_slug': 'ultrabooks',
                'description': 'A lightweight and efficient ultrabook.',
                'image': 'path_to_image/macbook_air.jpg',
                'original_price': 1199.99,
                'discount_percentage': 5.0,
                'meta_title': 'MacBook Air',
                'meta_description': 'A lightweight and efficient ultrabook by Apple.',
                'meta_tags': 'apple, macbook, air, ultrabook',
            },
            {
                'name': 'Dell XPS 13 Ultrabook',
                'category_slug': 'ultrabooks',
                'description': 'A high-end ultrabook with stunning display.',
                'image': 'path_to_image/dell_xps_13_ultrabook.jpg',
                'original_price': 1399.99,
                'discount_percentage': 10.0,
                'meta_title': 'Dell XPS 13 Ultrabook',
                'meta_description': 'A high-end ultrabook by Dell.',
                'meta_tags': 'dell, xps, ultrabook',
            },
            {
                'name': 'HP Envy 13',
                'category_slug': 'ultrabooks',
                'description': 'A stylish and compact ultrabook.',
                'image': 'path_to_image/hp_envy_13.jpg',
                'original_price': 999.99,
                'discount_percentage': 7.0,
                'meta_title': 'HP Envy 13',
                'meta_description': 'A stylish and compact ultrabook by HP.',
                'meta_tags': 'hp, envy, ultrabook',
            },
            # Desktops
            {
                'name': 'HP Pavilion Desktop',
                'category_slug': 'desktops',
                'description': 'A reliable and affordable desktop.',
                'image': 'path_to_image/hp_pavilion_desktop.jpg',
                'original_price': 599.99,
                'discount_percentage': 10.0,
                'meta_title': 'HP Pavilion Desktop',
                'meta_description': 'A reliable and affordable desktop by HP.',
                'meta_tags': 'hp, pavilion, desktop',
            },
            {
                'name': 'Dell Inspiron Desktop',
                'category_slug': 'desktops',
                'description': 'A versatile and powerful desktop.',
                'image': 'path_to_image/dell_inspiron_desktop.jpg',
                'original_price': 699.99,
                'discount_percentage': 12.0,
                'meta_title': 'Dell Inspiron Desktop',
                'meta_description': 'A versatile and powerful desktop by Dell.',
                'meta_tags': 'dell, inspiron, desktop',
            },
            {
                'name': 'Lenovo IdeaCentre',
                'category_slug': 'desktops',
                'description': 'A modern and efficient desktop.',
                'image': 'path_to_image/lenovo_ideacentre.jpg',
                'original_price': 799.99,
                'discount_percentage': 15.0,
                'meta_title': 'Lenovo IdeaCentre',
                'meta_description': 'A modern and efficient desktop by Lenovo.',
                'meta_tags': 'lenovo, ideacentre, desktop',
            },
            # Gaming Desktops
            {
                'name': 'Alienware Aurora',
                'category_slug': 'gaming-desktops',
                'description': 'A high-end gaming desktop.',
                'image': 'path_to_image/alienware_aurora.jpg',
                'original_price': 1999.99,
                'discount_percentage': 10.0,
                'meta_title': 'Alienware Aurora',
                'meta_description': 'A high-end gaming desktop by Alienware.',
                'meta_tags': 'alienware, aurora, gaming, desktop',
            },
            {
                'name': 'MSI Trident 3',
                'category_slug': 'gaming-desktops',
                'description': 'A compact and powerful gaming desktop.',
                'image': 'path_to_image/msi_trident_3.jpg',
                'original_price': 1299.99,
                'discount_percentage': 15.0,
                'meta_title': 'MSI Trident 3',
                'meta_description': 'A compact and powerful gaming desktop by MSI.',
                'meta_tags': 'msi, trident, gaming, desktop',
            },
            {
                'name': 'CyberPowerPC Gamer Xtreme',
                'category_slug': 'gaming-desktops',
                'description': 'A budget-friendly gaming desktop.',
                'image': 'path_to_image/cyberpowerpc_gamer_xtreme.jpg',
                'original_price': 999.99,
                'discount_percentage': 12.0,
                'meta_title': 'CyberPowerPC Gamer Xtreme',
                'meta_description': 'A budget-friendly gaming desktop by CyberPowerPC.',
                'meta_tags': 'cyberpowerpc, gamer, xtreme, gaming, desktop',
            },
            # Processors
            {
                'name': 'Intel Core i9',
                'category_slug': 'intel-processors',
                'description': 'A high-performance processor from Intel.',
                'image': 'path_to_image/intel_core_i9.jpg',
                'original_price': 499.99,
                'discount_percentage': 10.0,
                'meta_title': 'Intel Core i9',
                'meta_description': 'A high-performance processor by Intel.',
                'meta_tags': 'intel, core, i9, processor',
            },
            {
                'name': 'Intel Core i7',
                'category_slug': 'intel-processors',
                'description': 'A versatile processor from Intel.',
                'image': 'path_to_image/intel_core_i7.jpg',
                'original_price': 399.99,
                'discount_percentage': 12.0,
                'meta_title': 'Intel Core i7',
                'meta_description': 'A versatile processor by Intel.',
                'meta_tags': 'intel, core, i7, processor',
            },
            {
                'name': 'Intel Core i5',
                'category_slug': 'intel-processors',
                'description': 'An affordable processor from Intel.',
                'image': 'path_to_image/intel_core_i5.jpg',
                'original_price': 299.99,
                'discount_percentage': 15.0,
                'meta_title': 'Intel Core i5',
                'meta_description': 'An affordable processor by Intel.',
                'meta_tags': 'intel, core, i5, processor',
            },
        ]

        for product_data in products:
            category = Category.objects.filter(slug=product_data['category_slug']).first()
            if category:
                product, created = Product.objects.update_or_create(
                    slug=slugify(product_data['name']),
                    defaults={
                        'name': product_data['name'],
                        'category': category,
                        'description': product_data['description'],
                        'original_price': product_data['original_price'],
                        'discount_percentage': product_data['discount_percentage'],
                        'status': True,
                        'meta_title': product_data['meta_title'],
                        'meta_description': product_data['meta_description'],
                        'meta_tags': product_data['meta_tags'],
                    }
                )

                # Handling the image file
                image_path = product_data['image']
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        product.image.save(os.path.basename(image_path), File(image_file), save=True)

                self.stdout.write(self.style.SUCCESS(f'Successfully {"created" if created else "updated"} product: {product.name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Category with slug {product_data["category_slug"]} not found'))

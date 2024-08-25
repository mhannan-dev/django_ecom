from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Seed all data'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE('Seeding categories...'))
            call_command('seed_categories')

            self.stdout.write(self.style.NOTICE('Seeding products...'))
            call_command('seed_products')

            self.stdout.write(self.style.NOTICE('Seeding ratings...'))
            call_command('seed_ratings')

            self.stdout.write(self.style.NOTICE('Seeding inventory adjustments...'))
            call_command('seed_inventory_adjustments')

            self.stdout.write(self.style.SUCCESS('Successfully seeded all data'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding data: {str(e)}'))

from django.core.management.base import BaseCommand
from main.models import Product, InventoryAdjustment
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seed the inventory adjustments'

    def handle(self, *args, **kwargs):
        # Fetch all products
        products = list(Product.objects.all())

        if not products:
            self.stdout.write(self.style.ERROR('No products found in the database.'))
            return

        reasons = [
            'Initial Stock',
            'Restock',
            'Damaged Goods',
            'Returned Items',
            'Promotional Giveaway',
            'Inventory Correction',
        ]

        for product in products:
            # Create random inventory adjustments for each product
            number_of_adjustments = random.randint(1, 5)
            for _ in range(number_of_adjustments):
                quantity = random.randint(20, 50)
                reason = random.choice(reasons)
                adjustment_date = timezone.now() - timezone.timedelta(days=random.randint(0, 365))

                InventoryAdjustment.objects.create(
                    product=product,
                    quantity=quantity,
                    reason=reason,
                    date=adjustment_date,
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully created adjustment of {quantity} units for product: {product.name} on {adjustment_date}'))


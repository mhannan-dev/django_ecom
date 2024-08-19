from django.core.management.base import BaseCommand
from main.models import Product, Rating
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the ratings'

    def handle(self, *args, **kwargs):
        # Fetch all users and products
        users = list(User.objects.all())
        products = list(Product.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('No users found in the database.'))
            return

        if not products:
            self.stdout.write(self.style.ERROR('No products found in the database.'))
            return

        for product in products:
            # Seed random ratings for each product by different users
            number_of_ratings = random.randint(1, len(users))
            rating_users = random.sample(users, number_of_ratings)

            for user in rating_users:
                rating_value = random.randint(1, 5)
                rating, created = Rating.objects.update_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'rating': rating_value,
                        'created_at': timezone.now(),
                    }
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully {"created" if created else "updated"} rating: {rating_value} for product: {product.name} by user: {user.username}'))


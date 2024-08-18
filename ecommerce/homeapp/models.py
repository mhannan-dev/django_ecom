from django.db import models
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class InventoryAdjustment(models.Model):
    product = models.ForeignKey('Product', related_name='inventory_adjustments', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.quantity} units for {self.product.name} on {self.date}'

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    status = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField(null=True, blank=True)
    meta_tags = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)

    def discounted_price(self):
        return self.original_price * (1 - (self.discount_percentage / 100))

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.rating for rating in ratings) / ratings.count()
        return None

    def rating_count(self):
        return self.ratings.count()

    def get_current_inventory_quantity(self):
        adjustments = InventoryAdjustment.objects.filter(product=self)
        return sum(adjustment.quantity for adjustment in adjustments)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'Image for {self.product.name}'

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.rating} - {self.product.name}'


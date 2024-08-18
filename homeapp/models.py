from django.db import models
from django.utils import timezone

from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
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
            return sum(rating.value for rating in ratings) / ratings.count()
        return None

    def review_count(self):
        return self.ratings.count()

    def current_inventory_quantity(self):
        adjustments = InventoryAdjustment.objects.filter(product=self)
        return adjustments.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    def __str__(self):
        return self.name

class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Rating {self.value} for {self.product.name}'

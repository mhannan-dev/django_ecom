from django.contrib import admin
from .models import Product, Rating, Category

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_price', 'discount_percentage', 'discounted_price', 'average_rating', 'review_count')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [RatingInline]
    search_fields = ('name', 'description')
    list_filter = ('category',)

    def discounted_price(self, obj):
        return obj.discounted_price()
    discounted_price.short_description = 'Discounted Price'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'value', 'comment')
    list_filter = ('product', 'value') 
    search_fields = ('product__name', 'comment') 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status', 'parent')

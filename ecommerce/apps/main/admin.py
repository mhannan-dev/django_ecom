from django.contrib import admin
from django.utils.html import format_html

from apps.main.models import Category, InventoryAdjustment, Product, ProductImage, Rating, Slider


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'original_price', 'display_main_image', 'discount_percentage', 'current_inventory_quantity', 'status')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [RatingInline, ProductImageInline]
    search_fields = ('name', 'description')
    list_filter = ('category',)

    def discounted_price(self, obj):
        return obj.discounted_price()
    discounted_price.short_description = 'Discounted Price'

    def display_main_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return format_html('<img src="{}" width="50" height="50" />', 'https://via.placeholder.com/50')  
    display_main_image.short_description = 'Main Image'

    def current_inventory_quantity(self, obj):
        return obj.get_current_inventory_quantity()
    current_inventory_quantity.short_description = 'Current Inventory Quantity'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'rating', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status', 'parent')

@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'reason', 'date')
    list_filter = ('date', 'product')
    search_fields = ('product__name', 'reason')
    readonly_fields = ('date',)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'status', 'created_at', 'updated_at')
    list_editable = ('order', 'status')
    search_fields = ('title', 'subtitle')
    list_filter = ('status', 'created_at')
    ordering = ('order',)
    fields = ('title', 'subtitle', 'image', 'link_url', 'alt_text', 'order', 'status')
# Generated by Django 4.2.15 on 2024-08-18 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_product_inventory_quantity_inventoryadjustment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='inventory_quantity',
        ),
    ]

# Generated by Django 3.2.15 on 2023-08-17 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_auto_20230817_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantmenuitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='foodcartapp.product', verbose_name='продукт'),
        ),
        migrations.AlterField(
            model_name='restaurantmenuitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='foodcartapp.restaurant', verbose_name='ресторан'),
        ),
    ]
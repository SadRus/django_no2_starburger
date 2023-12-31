# Generated by Django 3.2.15 on 2023-08-17 17:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=200, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'Наличными'), ('online', 'Онлайн'), ('not_specified', 'Не указано')], db_index=True, default='not_specified', max_length=30, verbose_name='Тип оплаты'),
        ),
        migrations.AlterField(
            model_name='orderproductitem',
            name='quantity',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='restaurantmenuitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodcartapp.product', verbose_name='продукт'),
        ),
        migrations.AlterField(
            model_name='restaurantmenuitem',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodcartapp.restaurant', verbose_name='ресторан'),
        ),
    ]

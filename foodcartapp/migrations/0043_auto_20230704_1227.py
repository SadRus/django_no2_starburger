# Generated by Django 3.2.15 on 2023-07-04 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20230703_2139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'клиент', 'verbose_name_plural': 'клиенты'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderproductitem',
            options={'verbose_name': 'продукт в заказе', 'verbose_name_plural': 'продукты в заказе'},
        ),
    ]

# Generated by Django 3.2.15 on 2023-08-05 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_alter_order_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-status', 'id'], 'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
    ]

# Generated by Django 3.2.15 on 2023-07-18 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Комментарий'),
        ),
    ]

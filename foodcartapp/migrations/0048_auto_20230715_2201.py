# Generated by Django 3.2.15 on 2023-07-15 19:01

from django.db import migrations
from django.db.models import F, Subquery, OuterRef


def calculate_order_item_price(apps, schema_editor):
    OrderProductItem = apps.get_model('foodcartapp', 'OrderProductItem')
    OrderProductItem.objects.update(
        price=F('quantity') * Subquery(OrderProductItem.objects
                                                       .filter(pk=OuterRef('pk'))
                                                       .values('product__price')[:1])
    )


def move_backward(apps, schema_editor):
    OrderProductItem = apps.get_model('foodcartapp', 'OrderProductItem')
    OrderProductItem.objects.update(price=0)


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_orderproductitem_price'),
    ]

    operations = [
        migrations.RunPython(calculate_order_item_price, move_backward)
    ]
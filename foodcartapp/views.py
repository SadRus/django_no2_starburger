import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.test import APITestCase
from rest_framework.response import Response

from .models import (
    Product,
    Customer,
    Order,
    OrderProductItem,
)


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    raw_order = request.data
    order_products = raw_order.get('products', None)
    if not isinstance(order_products, list) or order_products == 0:
        return Response('products key not presented or not list', status=400)
    customer, _ = Customer.objects.get_or_create(
        firstname=raw_order['firstname'],
        lastname=raw_order['lastname'],
        defaults={
            'phonenumber': raw_order['phonenumber']
        }
    )
    order = Order.objects.create(
        address=raw_order['address'],
        customer=customer,
    )
    for raw_product in raw_order['products']:
        OrderProductItem.objects.create(
            order=order,
            product=Product.objects.get(pk=raw_product['product']),
            quantity=raw_product['quantity'],
        )
    return raw_order

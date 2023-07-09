import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ModelSerializer, CharField

from .models import (
    Product,
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


class OrderProductItemSerializer(ModelSerializer):
    class Meta:
        model = OrderProductItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderProductItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']


@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_order = serializer.validated_data
    print(validated_order)

    order = Order.objects.create(
        firstname=validated_order['firstname'],
        lastname=validated_order['lastname'],
        phonenumber=validated_order['phonenumber'],
        address=validated_order['address'],
    )
    for raw_product in validated_order['products']:
        OrderProductItem.objects.create(
            order=order,
            product=raw_product['product'],
            quantity=raw_product['quantity'],
        )
    return Response(request.data)

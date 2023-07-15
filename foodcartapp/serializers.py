from rest_framework.serializers import ModelSerializer

from .models import Order, OrderProductItem


class OrderProductItemSerializer(ModelSerializer):
    class Meta:
        model = OrderProductItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderProductItemSerializer(
        allow_empty=False,
        many=True,
        write_only=True,
    )

    class Meta:
        model = Order
        fields = ['id', 'products', 'firstname', 'lastname', 'phonenumber', 'address']

    def create(self, validated_data):
        raw_products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for raw_product in raw_products:
            OrderProductItem.objects.create(
                order=order,
                product=raw_product['product'],
                price=raw_product['product'].price * raw_product['quantity'],
                quantity=raw_product['quantity'],
            )
        return order

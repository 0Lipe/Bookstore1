from rest_framework import serializers
from product.models import Product
from product.serializers.product_serializer import ProductSerializer
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True, many=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ['product', 'total', 'user', 'product_id']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        product_data = validated_data.pop('product_id')
        user_data = validated_data.pop('user')

        order = Order.objects.create(user=user_data)
        order.products.set(product_data)  # Set the many-to-many relationship

        return order  # Corrected the typo here

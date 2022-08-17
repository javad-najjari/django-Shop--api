from .models import Order
from rest_framework import serializers
from store.serializers import ProductSerializer
from extensions.utils import persian_numbers_converter



class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('product', 'number', 'total_price')
    
    def get_total_price(self, obj):
        price_to_str = str(obj.number * obj.product.price)
        right_price = ''
        for num, i in zip(price_to_str[::-1], range(1, len(price_to_str)+1)):
            right_price += num
            if i % 3 == 0 and i != len(price_to_str):
                right_price += ','
        return persian_numbers_converter(right_price[::-1])
    

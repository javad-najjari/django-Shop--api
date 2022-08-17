from rest_framework import serializers
from .models import Category, Product, Comment
from extensions.utils import persian_numbers_converter
from accounts.serializers import UserSerializer



class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'slug', 'image')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('title', 'category', 'description', 'price', 'photo')
    
    
    def get_price(self, obj):
        price_to_str = str(obj.price)
        right_price = ''
        for num, i in zip(price_to_str[::-1], range(1, len(price_to_str)+1)):
            right_price += num
            if i % 3 == 0 and i != len(price_to_str):
                right_price += ','
        return persian_numbers_converter(right_price[::-1])
    

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Comment
        fields = ('author', 'reply', 'is_reply', 'body')
    
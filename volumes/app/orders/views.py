from .serializers import OrderSerializer
from orders.models import Order
from store.models import Product
from store.serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated




class CartAddView(APIView):
    def get(self, request, product_slug):
        try:
            global product
            product = Product.objects.get(slug=product_slug)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request, product_slug):
        user = request.user
        order = request.data
        try:
            if not Order.objects.filter(user=user, product=product).exists():
                Order.objects.create(
                    user = user,
                    product = product,
                    number = order['number']
                )
            else:
                new_order = Order.objects.get(user=user, product=product)
                new_order.number += order['number']
                new_order.save()
        except KeyError:
            content = {'Error': "You must send us the field 'number' "}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = ProductSerializer(product)
        return Response(serializer.data)



class CartRemoveView(APIView):
    def get(self, request, order_id, count):
        try:
            order = Order.objects.get(id=order_id)
            product = order.product
        except Order.DoesNotExist:
            content = {'Error': 'product not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if order != None and request.user == order.user:
            if order.number == 1 or count == 'all':
                order.delete()
            elif count == 'one':
                order.number -= 1
                order.save()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        


class MyCardView(ListAPIView):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


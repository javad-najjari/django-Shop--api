from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Product, Category, Comment
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer




class CategoriesView(ListAPIView):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductsView(APIView):
    def get(self, request):
        if request.GET.get('search'):
            products = Product.objects.filter(title__contains=request.GET['search'])
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)


class CategoryProductsView(APIView):
    def get(self, request, slug):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        my_data = Product.objects.filter(category=category)
        products = ProductSerializer(my_data, many=True, context={'request': request})
        return Response(products.data)


class ProductDetailView(APIView):
    def get(self, request, product_slug):
        try:
            global product
            product = Product.objects.get(slug=product_slug)
            comments = product.product_comments.filter(is_reply=False)
        except Product.DoesNotExist:
            content = {'Error': 'product not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductSerializer(product, context={'request': request})
        comments_serializer = CommentSerializer(comments, context={'request': request}, many=True)
        global my_data
        my_data = {'product': product_serializer.data, 'comments': comments_serializer.data}
        return Response(my_data)
    
    def post(self, request, *args, **kwargs):
        comment = request.data
        try:
            Comment.objects.create(
                product = product,
                author = request.user,
                is_reply = False,
                body = comment['body'],
            )
        except KeyError:
            content = {'Error': "You must send us the field 'body' "}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(my_data)


class AddReplyView(APIView):
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            content = {'Error': 'comment not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        reply_comment = request.data
        
        try:
            Comment.objects.create(
                author = request.user,
                product = comment.product,
                reply = comment,
                body = reply_comment['body'],
                is_reply = True,
            )
        except KeyError:
            content = {'Error': "You must send us the field 'body' "}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment)
        return Response(serializer.data)


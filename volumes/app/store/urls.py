from django.urls import path
from .views import (
    CategoriesView, CategoryProductsView, ProductDetailView, ProductsView, AddReplyView
)


app_name = 'store'
urlpatterns = [
    path('', CategoriesView.as_view(), name='home'),
    path('all-products/', ProductsView.as_view(), name='list'),
    path('category/<slug:slug>/', CategoryProductsView.as_view(), name='category-products'),
    path('detail/<slug:product_slug>/', ProductDetailView.as_view(), name='detail'),
    path('reply-to-comment/<int:comment_id>/', AddReplyView.as_view(), name='add_reply'),
]

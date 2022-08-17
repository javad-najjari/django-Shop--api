from django.urls import path
from .views import CartAddView, MyCardView, CartRemoveView



app_name = 'orders'
urlpatterns = [
    path('add-to-card/<slug:product_slug>', CartAddView.as_view(), name='add_order'),
    path('delete/<int:order_id>/<count>', CartRemoveView.as_view(), name='remove_order'),
    path('card', MyCardView.as_view(), name='user_card'),
]

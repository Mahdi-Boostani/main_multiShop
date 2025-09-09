from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detail', views.CartDetailView.as_view(), name='cart_Detail'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart_add'),
    path('add/<str:pk>', views.CartDeleteView.as_view(), name='cart_delete'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='cart_order_detail'),
    path('add', views.OrderCreationView.as_view(), name='cart_order_creation'),
    path('discount/<int:pk>', views.ApplyDiscountView.as_view(), name='apply_discount'),
]

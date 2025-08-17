from django.urls import path
from .views import CustomLoginView, product_list, edit_product, delete_product
from django.contrib.auth.views import LogoutView

app_name = 'products'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', product_list, name='product_list'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:pk>/', delete_product, name='delete_product'),
    path('logout/', LogoutView.as_view(), name='logout'),

]

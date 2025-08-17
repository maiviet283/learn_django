from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Product

# Trang login riêng
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return reverse_lazy('products:product_list')  # Admin về danh sách sản phẩm
        elif user.groups.filter(name='Nhân viên').exists():
            return reverse_lazy('products:product_list')
        elif user.groups.filter(name='Khách hàng').exists():
            return reverse_lazy('products:product_list')  # Hoặc trang riêng
        return reverse_lazy('products:product_list')  # fallback

# Danh sách sản phẩm
@login_required
def product_list(request):
    products = Product.objects.all()
    user = request.user
    is_admin = user.groups.filter(name='Admin').exists()
    is_staff = user.groups.filter(name='Nhân viên').exists()
    is_customer = user.groups.filter(name='Khách hàng').exists()
    return render(request, 'products/product_list.html', {
        'products': products,
        'is_admin': is_admin,
        'is_staff': is_staff,
        'is_customer': is_customer,
    })


# Sửa sản phẩm
@login_required
@permission_required('products.change_product', raise_exception=True)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.save()
        return redirect('products:product_list')
    return render(request, 'products/edit_product.html', {'product': product})

# Xoá sản phẩm
@login_required
@permission_required('products.delete_product', raise_exception=True)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/confirm_delete.html', {'product': product})

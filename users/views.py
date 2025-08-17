from django.shortcuts import render, redirect
from .models import Customer
from django.contrib.auth.hashers import check_password

# Create your views here.
def login(request):
    if request.session.get('customer_id'):
        return redirect('home:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user = Customer.objects.get(username=username) # 1 truy van
            if check_password(password, user.password):
                request.session['customer_id'] = user.id # 1 truy van
                return redirect('home:index') # <== Trả về HTTP 302 Redirect
            else:
                return render(request, 'users/login.html', {
                    'error': 'Tên đăng nhập hoặc mật khẩu không đúng.'
                })
        except Customer.DoesNotExist:
            return render(request, 'users/login.html', {
                'error': 'Tên đăng nhập hoặc mật khẩu không đúng.'
            })
    return render(request, 'users/login.html')


def logout(request):
    try:
        request.session.pop('customer_id', None)
    except Exception:
        pass
    return redirect('home:index')
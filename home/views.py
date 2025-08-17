from django.shortcuts import render
from users.models import Customer
from django.contrib import messages


# Create your views here.
def index(request):
    id = request.session.get('customer_id')
    user = None

    if id:
        try:
            user = Customer.objects.get(id=id)
        except Exception:
            messages.error(request, "Error loading user information")
            user = None

    return render(request, 'home/index.html',{
        'user':user
    })
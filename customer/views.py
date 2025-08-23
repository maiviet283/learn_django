from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    customer = request.user.customer
    print(customer)
    return HttpResponse('Hello baby')
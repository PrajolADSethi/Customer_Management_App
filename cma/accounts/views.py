from django.shortcuts import render
# from django.http import HttpResponse
# Create your views here.
from .models import *
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="delivered").count()
    orders_pending = orders.filter(status="pending").count()
    context = {'customers':customers,'orders':orders,
    'total_orders':total_orders,'orders_delivered':orders_delivered,'orders_pending':orders_pending}
    return render(request,'accounts/dashboard.html',context)

def product(request):
    product = Product.objects.all()
    return render(request,'accounts/products.html', {'product':product})

def customer(request):
    # customer= Customer.objects.all()
    return render(request,'accounts/customer.html',{'customer':customer})

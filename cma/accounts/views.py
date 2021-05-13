from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
# from django.http import HttpResponse
# Create your views here.
from .models import *
from .form import OrderForm
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

def customer(request, pk):
    customers= Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    total_orders = orders.count()
    context = {'customers':customers,'orders':orders,
    'total_orders':total_orders}
    return render(request,'accounts/customer.html',context)

def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=10)
    customers = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance = customers)
    # form = OrderForm(initial = {'customers':customers})
    if request.method == 'POST':
        formset = OrderForm(request.POST,instance = customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def update_order(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request, 'accounts/delete_order.html', context)

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse
# Create your views here.
from .models import *
from .form import OrderForm ,CreateUserForm


# def registerPage(request):
# 	if request.user.is_authenticated:
# 		return redirect('home')
# 	else:
# 		form = CreateUserForm()
# 		if request.method == 'POST':
# 			form = CreateUserForm(request.POST)
# 			if form.is_valid():
# 				form.save()
# 				user = form.cleaned_data.get('username')
# 				messages.success(request, 'Account was created for ' + user)
#
# 				return redirect('login')
#
#
# 		context = {'form':form}
# 		return render(request, 'accounts/register.html', context)
#
# def loginPage(request):
# 	if request.user.is_authenticated:
# 		return redirect('home')
# 	else:
# 		if request.method == 'POST':
# 			username = request.POST.get('username')
# 			password =request.POST.get('password')
#
# 			user = authenticate(request, username=username, password=password)
#
# 			if user is not None:
# 				login(request, user)
# 				return redirect('home')
# 			else:
# 				messages.info(request, 'Username OR password is incorrect')
#
# 		context = {}
# 		return render(request, 'accounts/login.html', context)
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for "+ user)
            return redirect('login')

    context={'form': form}
    return render(request, 'accounts/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is invalid')
    context={}
    return render(request, 'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="delivered").count()
    orders_pending = orders.filter(status="pending").count()
    context = {'customers':customers,'orders':orders,
    'total_orders':total_orders,'orders_delivered':orders_delivered,'orders_pending':orders_pending}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
def product(request):
    product = Product.objects.all()
    return render(request,'accounts/products.html', {'product':product})

@login_required(login_url='login')
def customer(request, pk):
    customers= Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs
    context = {'customers':customers,'orders':orders,
    'total_orders':total_orders,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
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

@login_required(login_url='login')

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

@login_required(login_url='login')
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request, 'accounts/delete_order.html', context)

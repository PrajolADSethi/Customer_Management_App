from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse('home')

def product(request):
    return HttpResponse('product')

def customer(request):
    return HttpResponse('customer')

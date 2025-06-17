from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

#index is the home page
# /proucts should map to this func
def index(request):
    products = Product.objects.all()
    return render(request,'index.html',
                  {'products': products})


def new(request):
    return HttpResponse('Hello world!, this is the new products page')
    

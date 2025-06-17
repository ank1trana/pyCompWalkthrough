from django.shortcuts import render
from django.http import HttpResponse


#index is the home page
# /proucts should map to this func
def index(request):
    return HttpResponse('Hello world!')


def new(request):
    return HttpResponse('Hello world!, this is the new products page')
    

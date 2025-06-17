from django.urls import path
from . import views
#'' in path represents root of the app

urlpatterns = [
    path('',views.index), 
    path('new',views.new)
]

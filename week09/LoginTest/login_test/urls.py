from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_home),
    path('my_login', views.my_login),
    path('my_logout', views.my_logout)
]
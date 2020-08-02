from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_gt_3, name='index_url'),
    path('search/', views.search_comment, name='search_url'),
]
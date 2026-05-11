from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coleta/', views.coleta_list, name='coleta_list'),
]
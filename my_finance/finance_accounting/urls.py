from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_operation/', views.add_operation, name='add_operation'),
    path('detail/', views.detail, name='detail'),
]
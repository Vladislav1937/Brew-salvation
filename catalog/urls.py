from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.coffee_list, name='coffee_list'),
    path('<slug:slug>/', views.coffee_detail, name='coffee_detail'),
]
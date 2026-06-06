from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('category/<slug:category_slug>/', views.article_list, name='category_filter'),
     path('category/<slug:category_slug>/', views.article_list, name='article_list_by_category'),
    path('calculator/', views.brewing_calculator, name='brewing_calculator'),
    path('like/<slug:slug>/', views.like_article, name='like_article'),# ← ПОДНЯЛИ ВВЕРХ
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]
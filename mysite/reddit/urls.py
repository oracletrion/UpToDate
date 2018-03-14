from django.urls import path

from . import views

urlpatterns = [
    path('', views.form, name='index'),
    path('form/', views.form, name='form'),
    path('search/', views.search, name='search'),
    path('<str:sub_name>/', views.reddit_test, name='reddit'),
]

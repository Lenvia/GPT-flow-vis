"""
@file: urls.py
@author: Runpu
@time: 2023/5/19 20:58
"""
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.my_view, name='my_view'),
    path('test/', views.test, name='test'),
    path('upload/', views.uploadNC, name='upload'),
]

"""

作者：崔杰
日期：2021年07月08日
"""
from . import views
from django.urls import path

urlpatterns = [
    path('index',views.index_view),
]

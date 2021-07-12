"""

作者：崔杰
日期：2021年07月09日
"""
from . import views
from django.urls import path

urlpatterns = [
    path("notes_list",views.list_view),
    path("note_add",views.add_view),
]
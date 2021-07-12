"""

作者：崔杰
日期：2021年07月07日
"""

from . import views
from django.urls import path

urlpatterns = [
    path('reg',views.reg_view),
    path('login',views.login_view),
    path('logout',views.logout_view)
]

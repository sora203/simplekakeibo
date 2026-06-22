from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ★これを追加！
    path('delete/<int:pk>/', views.delete_expense, name='delete'),
]
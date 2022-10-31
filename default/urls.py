from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('delete/', views.delete_view, name="delete_view"),
]
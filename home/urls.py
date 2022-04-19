from django.urls import path
from home import views

urlpatterns = [
    path('', views.home),
    path('if/', views.insertFage),
    path('i/', views.insert),
    path('delete/', views.dataDelete)
]
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home),
    path('onoff/', views.onoff),
    path('changeStatus/', views.changeStatus, name="changeStatus"),
    path('changeMethod/', views.changeMethod, name="changeMethod"),
    path('transHistory/', views.transHistory),

    path('if/', views.insertFage),
    path('i/', views.insert)
]
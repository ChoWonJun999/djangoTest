from django.urls import path
from home import views

urlpatterns = [
    path('login/', views.login_html),
    path('goHome/', views.goHome, name="goHome"),
    path('join/', views.user_join_html),
    path('checkId/', views.checkId, name="checkId"),
    path('joinFinish/', views.joinFinish),
    path('logout/', views.logout),

    path('', views.home_html),
    path('transHistory/', views.transHistory_html),
    path('onoff/', views.onoff_html),
    path('changeStatus/', views.changeStatus, name="changeStatus"),
    path('changeMethod/', views.changeMethod, name="changeMethod"),

    path('if/', views.insertFage),
    path('i/', views.insert)
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('delete/<int:id>/', views.delete, name = 'delete'),
    path('new-user/', views.signup),
    path('logout/', views.logoutuser, name = 'logout'),
    path('login/', views.loginuser, name= 'loginuser')
]

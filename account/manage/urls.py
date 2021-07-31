from django.urls import path, include
from account.manage import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_add'),
    path('users/<int:id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:id>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:id>/password/', views.user_password, name='user_password'),
]
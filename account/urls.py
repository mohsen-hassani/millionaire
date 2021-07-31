from django.urls.conf import path, include
from django.contrib.auth import views as auth
from account import views

app_name = 'account'
urlpatterns = [
    path('manage/', include('account.manage.urls')),
    path('login/', auth.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('roles/', views.manage_roles, name='manage_roles'),
]

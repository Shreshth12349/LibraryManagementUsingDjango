from django import urls
from django.urls import path
from . import views


urlpatterns = [\
    path('', views.redirect_to_login, name='redirect_to_login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]


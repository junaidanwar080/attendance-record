from django.urls import path
from authenticate import views

urlpatterns = [
    # User Login 
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
]

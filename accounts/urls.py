
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, UserProfileView, CustomTokenObtainPairView

)

urlpatterns = [
   
  path("auth/register" , RegisterView.as_view() , name='register'),
  path("auth/" , CustomTokenObtainPairView.as_view() , name= 'login' ),
  path("auth/refresh" , TokenRefreshView.as_view() , name= 'refresh'), 
  path("auth/userprofile" , UserProfileView.as_view() , name='userprofile')
]

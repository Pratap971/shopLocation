from django.urls import path

from . import views
from .views import Shopget, ShopUpdate,RegisterAPI,LoginAPI,LogoutApiView,SocialAuthView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('nearby/<int:latitude>/<int:langitude>/', Shopget.as_view()),
    path('add/', ShopUpdate.as_view(),name="add_shop_data"),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/',LoginAPI.as_view(),name='login'),
    path('logout/',LogoutApiView.as_view(),name='logout'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/<backend>/', SocialAuthView.as_view()),
]
  

from django.urls import path
from home.views import  UserLoginView, UserProfileView, UserRegistrationView,ProfileCrud
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update/', ProfileCrud.as_view(), name='update'),
    path('update/<int:pk>/', ProfileCrud.as_view(), name='update'),
]
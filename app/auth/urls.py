from django.urls import path
from .views import RegisterUser, LoginUser


# URL configuration of the store app
urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view())
]

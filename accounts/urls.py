from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from accounts.views import CreateAccountView

urlpatterns = [
    path("accounts/", CreateAccountView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
]

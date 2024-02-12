from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "api"

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "register/", views.UserRegister.as_view(), name='register'
    ),
    path(
        "login/", views.UserLogin.as_view(), name='login'
    ),
    path(
        "logout/", views.UserLogout.as_view(), name='logout'
    ),
    path(
        "data/", views.Data.as_view(), name='data'
    ),
]

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, ProfileView, UserDeleteView,SendEmailVerificationCodeView,VerifyEmailView,RecoveryConfirmView,RecoveryRequestView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/delete/", UserDeleteView.as_view(), name="profile-delete"),
path("send-verification-code/", SendEmailVerificationCodeView.as_view(), name="send-verification-code"),
path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
path("recovery/request/", RecoveryRequestView.as_view(), name="recovery-request"),
path("recovery/confirm/", RecoveryConfirmView.as_view(), name="recovery-confirm"),
]
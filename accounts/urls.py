from django.urls import path
from .views import RegisterView, ProfileView, UserDeleteView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/delete/", UserDeleteView.as_view(), name="profile-delete"),
]
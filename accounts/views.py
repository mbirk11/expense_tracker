from django.contrib.auth import get_user_model
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import random

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    SendVerificationCodeSerializer,
    EmailVerificationSerializer,
    RecoveryRequestSerializer,
    RecoveryConfirmSerializer,
)

User = get_user_model()


@extend_schema(tags=["Authentication & User Management"])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


@extend_schema(tags=["Authentication & User Management"])
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Authentication & User Management"])
class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Authentication & User Management"])
class SendEmailVerificationCodeView(APIView):
    serializer_class = SendVerificationCodeSerializer

    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = str(random.randint(1000, 9999))

        cache.set(f"email_verification_{email}", code, timeout=3600)

        return Response(
            {
                "message": "Verification code sent successfully.",
                "code": code,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication & User Management"])
class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        saved_code = cache.get(f"email_verification_{email}")

        if saved_code != code:
            return Response(
                {"error": "Invalid or expired verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)
        user.is_email_verified = True
        user.save()

        cache.delete(f"email_verification_{email}")

        return Response(
            {"message": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication & User Management"])
class RecoveryRequestView(APIView):
    serializer_class = RecoveryRequestSerializer

    def post(self, request):
        serializer = RecoveryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        recovery_answer = serializer.validated_data["recovery_answer"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.recovery_answer != recovery_answer:
            return Response(
                {"error": "Recovery answer is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        code = str(random.randint(1000, 9999))
        cache.set(f"password_recovery_{email}", code, timeout=3600)

        return Response(
            {
                "message": "Recovery code generated successfully.",
                "code": code,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication & User Management"])
class RecoveryConfirmView(APIView):
    serializer_class = RecoveryConfirmSerializer

    def post(self, request):
        serializer = RecoveryConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        new_password = serializer.validated_data["new_password"]

        saved_code = cache.get(f"password_recovery_{email}")

        if saved_code != code:
            return Response(
                {"error": "Invalid or expired recovery code."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        cache.delete(f"password_recovery_{email}")

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )
from django.contrib.auth import get_user_model
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from django.core.cache import cache
from .serializers import RegisterSerializer, UserProfileSerializer,SendVerificationCodeSerializer,EmailVerificationSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class SendEmailVerificationCodeView(APIView):
    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = str(random.randint(1000, 9999))

        cache.set(f"email_verification_{email}", code, timeout=3600)

        return Response({
            "message": "Verification code sent successfully.",
            "code": code
        }, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        saved_code = cache.get(f"email_verification_{email}")

        if saved_code != code:
            return Response({
                "error": "Invalid or expired verification code."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        user.is_email_verified = True
        user.save()

        cache.delete(f"email_verification_{email}")

        return Response({
            "message": "Email verified successfully."
        }, status=status.HTTP_200_OK)

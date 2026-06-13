from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "password",
            "password_confirm",
            "recovery_question",
            "recovery_answer",
            "is_email_verified",
        ]
        read_only_fields = ["id", "is_email_verified"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match."
            })
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_phone(self, value):
        if not value.startswith("+"):
            raise serializers.ValidationError("Phone number must start with '+'.")
        if len(value) < 9:
            raise serializers.ValidationError("Phone number is too short.")
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "recovery_question",
            "is_email_verified",
        ]
        read_only_fields = ["id", "email", "is_email_verified"]


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RecoveryRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    recovery_answer = serializers.CharField(max_length=255)


class RecoveryConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
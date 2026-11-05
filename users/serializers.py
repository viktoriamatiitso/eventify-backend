from django.contrib.auth.models import User
from rest_framework import serializers
import re
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100, 
        validators=[UniqueValidator(queryset=User.objects.all(), message="Користувач з таким username вже існує")]
    )
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset= User.objects.all(), message="Користувач з таким email вже існує")]
    )
    password = serializers.CharField(write_only=True, max_length=100, min_length=8)
    password_confirmation = serializers.CharField(write_only=True, max_length=100, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "password_confirmation"]

    def validate(self, attrs):
        if attrs.get("password") !=attrs.get("password_confirmation"):
            raise serializers.ValidationError({"password_confirmation": "Паролі не збігаються!"})
        return attrs
    
    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Пароль має містити хоча б одну велику літеру [A-Z]")
        if not re.search(r"[a-z]", value): 
            raise serializers.ValidationError("Пароль має містити хоча б одну маленьку літеру [a-z]")
        if not re.search(r"[!@#$%^&*]", value): 
            raise serializers.ValidationError("Пароль має містити хоча б один спеціальний символ [!@#$%^&*]")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Пароль має містити хоча б одну цифру[0-9]")
        return value
    
    def create(self, data):
        data.pop("password_confirmation")
        user = User.objects.create_user(
            username=data["username"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data["email"],
            password=data["password"],
        )
        return user
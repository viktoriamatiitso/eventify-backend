from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from .serializers import RegisterSerializer, UserSerializer

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

# Create your views here.

logger = logging.getLogger(__name__)

@extend_schema(
    tags=["auth"],
    summary="Реєстрація нового користувача",
    description="Створює нового користувача. Автентифікація не потрібна",
    auth=[],
    responses={
        201: RegisterSerializer,
        400: OpenApiResponse(
            description="Помилка валідації: username/email вже існують, паролі не збігаються, слабкий пароль"
        ),
    },
    examples=[
        OpenApiExample(
            "Приклад запиту",
            request_only=True,
            value={
                "username": "user123",
                "first_name": "User",
                "last_name": "Example",
                "email": "user123@example.com",
                "password": "Str0ngPass!",
                "password_confirmation": "Str0ngPass!",
            },
        ),
    ],
)

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

@extend_schema_view(
    get=extend_schema(
        tags=["users"],
        summary="Отримати профіль користувача",
        description="Потрібен JWT-токен: `Authorization: Bearer <access>`",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Токен відсутній або невалідний"),
            404: OpenApiResponse(description="Користувача не знайдено"),
        },
        examples=[
            OpenApiExample(
                "Приклад відповіді",
                response_only=True,
                status_codes=["200"],
                value={
                    "id": 1,
                    "username": "user123",
                    "first_name": "User",
                    "last_name": "Example",
                    "email": "user123@example.com",
                },
            ),
        ],
    ),
    put=extend_schema(
        tags=["users"],
        summary="Оновити власний профіль",
        description="Потрібен JWT-токен. Редагувати можна лише власний профіль",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            401: OpenApiResponse(description="Токен відсутній або невалідний"),
            403: OpenApiResponse(description="Спроба змінити чужий профіль"),
            404: OpenApiResponse(description="Користувача не знайдено"),
        },
        examples=[
            OpenApiExample(
                "Приклад запиту",
                request_only=True,
                value={
                    "username": "user123",
                    "first_name": "User",
                    "last_name": "Example",
                    "email": "user123@example.com",
                },
            ),
            OpenApiExample(
                "Приклад відповіді",
                response_only=True,
                status_codes=["200"],
                value={
                    "id": 1,
                    "username": "user123",
                    "first_name": "User",
                    "last_name": "Example",
                    "email": "user123@example.com",
                },
            ),
        ],
    ),
)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        logger.debug(f"Користувач id={request.user.id} запитує профіль id={id}")
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)

        if request.user != user:
            logger.warning(f"Відмова: користувач id={request.user.id} намагався змінити профіль id={id}")
            return Response(
                {"error": "Ви не маєте прав редагувати цей профіль"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Користувач id={user.id} оновив свій профіль")
        return Response(serializer.data)

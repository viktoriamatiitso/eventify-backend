from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from .models import Artist, Event, Venue
from .serializers import (
    ArtistSerializer,
    EventSerializer,
    VenueSerializer,
)


# Create your views here.

logger = logging.getLogger(__name__)

E400 = OpenApiResponse(description="Невалідні дані")
E401 = OpenApiResponse(description="Токен відсутній або невалідний")
E403 = OpenApiResponse(description="Потрібні права адміністратора")
E409 = OpenApiResponse(description="Є пов'язані дані, видалити неможливо")

@extend_schema_view(
    get=extend_schema(
        tags=["events"],
        summary="Список подій",
        description="Публічний ендпоінт, автентифікація не потрібна",
        auth=[],
        responses={200: EventSerializer(many=True)},
    ),
    post=extend_schema(
        tags=["events"],
        summary="Створити подію",
        description="Створити подію може лише адміністратор. Потрібен JWT токен",
        request=EventSerializer,
        responses={201: EventSerializer, 400: E400, 401: E401, 403: E403},
    ),
)

class EventList(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        logger.debug("Запит списку подій")
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        logger.info(f"Адміністратор id={request.user.id} створив подію id={event.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema_view(
    get=extend_schema(
        tags=["events"],
        summary="Отримати подію",
        description="Публічний ендпоінт, автентифікація не потрібна",
        auth=[],
        responses={200: EventSerializer, 404: OpenApiResponse(description="Подію не знайдено")},
    ),
    put=extend_schema(
        tags=["events"],
        summary="Оновити подію",
        description="Оновити подію може лише адміністратор. Потрібен JWT токен",
        request=EventSerializer,
        responses={200: EventSerializer, 400: E400, 401: E401, 403: E403, 404: OpenApiResponse(description="Подію не знайдено")},
    ),
    delete=extend_schema(
        tags=["events"],
        summary="Видалити подію",
        description="Видалити подію може лише адміністратор. Потрібен JWT токен",
        responses={204: OpenApiResponse(description="Подію видалено"), 401: E401, 403: E403, 404: OpenApiResponse(description="Подію не знайдено"), 409: E409},
    ),
)

class EventDetail(APIView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, id):
        logger.debug(f"Запит події id={id}")
        event = get_object_or_404(Event, id=id)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, id):
        event = get_object_or_404(Event, id=id)
        serializer = EventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        logger.info(f"Адміністратор id={request.user.id} оновив подію id={event.id}")
        return Response(serializer.data)

    def delete(self, request, id):
        event = get_object_or_404(Event, id=id)
        try:
            event.delete()
        except ProtectedError:
            logger.warning(f"Подію id={id} не видалено: є пов'язані дані")
            return Response(
                {
                    "error": "Неможливо видалити об'єкт, оскільки з ним пов'язані інші дані"
                },
                status=status.HTTP_409_CONFLICT,
            )
        logger.info(f"Адміністратор id={request.user.id} видалив подію id={id}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArtistList(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        logger.debug("Запит списку артистів")
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = serializer.save()
        logger.info(f"Адміністратор id={request.user.id} створив артиста id={artist.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArtistDetail(APIView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, id):
        logger.debug(f"Запит артиста id={id}")
        artist = get_object_or_404(Artist, id=id)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request, id):
        artist = get_object_or_404(Artist, id=id)
        serializer = ArtistSerializer(artist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Адміністратор id={request.user.id} оновив артиста id={artist.id}")
        return Response(serializer.data)

    def delete(self, request, id):
        artist = get_object_or_404(Artist, id=id)
        try:
            artist.delete()
        except ProtectedError:
            logger.warning(f"Артиста id={id} не видалено: є пов'язані дані")
            return Response(
                {
                    "error": "Неможливо видалити об'єкт, оскільки з ним пов'язані інші дані"
                },
                status=status.HTTP_409_CONFLICT,
            )
        logger.info(f"Адміністратор id={request.user.id} видалив артиста id={id}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class VenueList(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        logger.debug("Запит списку майданчиків")
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VenueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venue = serializer.save()
        logger.info(f"Адміністратор id={request.user.id} створив майданчик id={venue.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VenueDetail(APIView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, id):
        logger.debug(f"Запит майданчика id={id}")
        venue = get_object_or_404(Venue, id=id)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    def put(self, request, id):
        venue = get_object_or_404(Venue, id=id)
        serializer = VenueSerializer(venue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Адміністратор id={request.user.id} оновив майданчик id={venue.id}")
        return Response(serializer.data)

    def delete(self, request, id):
        venue = get_object_or_404(Venue, id=id)
        try:
            venue.delete()
        except ProtectedError:
            logger.warning(f"Майданчик id={id} не видалено: є пов'язані дані")
            return Response(
                {
                    "error": "Неможливо видалити об'єкт, оскільки з ним пов'язані інші дані"
                },
                status=status.HTTP_409_CONFLICT,
            )
        logger.info(f"Адміністратор id={request.user.id} видалив майданчик id={id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import render, get_object_or_404
from .models import Category, Artist, Venue, Event
from .serializers import CategorySerializer, ArtistSerializer, VenueSerializer, EventSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from  django.db.models import ProtectedError
# Create your views here.

class EventList(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EventSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class EventDetail(APIView):
    def get(self, request, id):
        event = get_object_or_404(Event, id=id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def put(self, request, id):
        event = get_object_or_404(Event, id=id)
        serializer = EventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        event = get_object_or_404(Event, id=id)
        try:
            event.delete()
        except ProtectedError:
            return Response(
                {"error": "Неможливо видалити об'єкт, оскільки з ним пов'язані інші дані"},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
        
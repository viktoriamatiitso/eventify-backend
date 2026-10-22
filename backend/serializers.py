from rest_framework import serializers
from .models import Category, Artist, Venue, Event

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ArtistSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Artist
        fields = "__all__"

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "description", "city", "address"]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event 
        fields = ["id", "title", "description", "price", "date", "category", "artist", "venue"]
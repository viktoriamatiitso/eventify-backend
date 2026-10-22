from rest_framework import serializers
from .models import Category, Artist, Venue, Event
from django.utils import timezone

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

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ціна не може бути від'ємною")
        return value

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Не можна додавати минувші події")
        return value
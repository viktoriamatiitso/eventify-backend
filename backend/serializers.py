from django.utils import timezone
from rest_framework import serializers

from .models import Artist, Category, Event, Venue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class EventForSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "date", "price"]


class ArtistSerializer(serializers.ModelSerializer):
    events = EventForSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ["id", "name", "description", "events"]


class VenueSerializer(serializers.ModelSerializer):
    events = EventForSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = ["id", "name", "description", "city", "address", "events"]


class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    artist = ArtistSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source="artist", write_only=True
    )
    venue_id = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all(), source="venue", write_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "price",
            "date",
            "category",
            "artist",
            "venue",
            "category_id",
            "artist_id",
            "venue_id",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Ціна не може бути від'ємною")
        return value

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Не можна додавати минувші події")
        return value

from django.contrib import admin
from .models import Category, Artist, Venue, Event
# Register your models here.

admin.site.register(Category)
admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Event)
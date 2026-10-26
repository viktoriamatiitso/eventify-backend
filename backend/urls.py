from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.EventList.as_view()),
    path("events/<int:id>/", views.EventDetail.as_view()),
    path("artists/", views.ArtistList.as_view()),
    path("artists/<int:id>/", views.ArtistDetail.as_view()),
    path("venues/", views.VenueList.as_view()),
    path("venues/<int:id>/", views.VenueDetail.as_view())
]
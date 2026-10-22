from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.EventList.as_view()),
    path("events/<int:id>", views.EventDetail.as_view()),
]
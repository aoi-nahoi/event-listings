from __future__ import annotations

from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list_view, name="event_list"),
    path("events/new/", views.event_create_view, name="event_create"),
    path("events/<int:event_id>/", views.event_detail_view, name="event_detail"),
    path("events/<int:event_id>/bookmarks/", views.bookmark_create_view, name="bookmark_create"),
    path("seed-demo/", views.seed_demo_view, name="seed_demo"),
    path("partials/events/", views.event_list_partial, name="event_list_partial"),
]

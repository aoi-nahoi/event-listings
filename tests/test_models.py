from datetime import date

import pytest
from django.contrib.auth.models import User

from events_app.models import Bookmark, Category, Event


@pytest.mark.django_db
def test_event_absolute_url():
    user = User.objects.create_user(username="sota")
    category = Category.objects.create(name="Lecture", slug="lecture")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Django lecture",
        description="Intro session",
        date=date(2026, 8, 1),
        location="Room M1",
    )

    assert event.get_absolute_url() == f"/events/{event.id}/"


@pytest.mark.django_db
def test_bookmark_belongs_to_event():
    user = User.objects.create_user(username="sota")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Campus meetup",
        description="Meet new students",
        date=date(2026, 8, 2),
        location="Cafeteria",
    )
    bookmark = Bookmark.objects.create(event=event, attendee_name="Aoi", note="I want to join")

    assert list(event.bookmarks.all()) == [bookmark]

from datetime import date

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from events_app.models import Bookmark, Category, Event
from events_app.selectors import EventFilters, published_events
from events_app.services import create_bookmark, create_event, seed_demo_content


@pytest.mark.django_db
def test_create_event_service():
    user = User.objects.create_user(username="sota")
    category = Category.objects.create(name="Workshop", slug="workshop")

    event = create_event(
        author=user,
        category=category,
        title="  Portfolio workshop  ",
        description="  Build a small portfolio  ",
        date=date(2026, 8, 3),
        location="  Lab 4  ",
        status=Event.Status.PUBLISHED,
    )

    assert event.title == "Portfolio workshop"
    assert event.description == "Build a small portfolio"
    assert event.location == "Lab 4"
    assert event.author == user


@pytest.mark.django_db
def test_create_bookmark_service():
    user = User.objects.create_user(username="sota")
    category = Category.objects.create(name="Concert", slug="concert")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Acoustic night",
        description="Music event",
        date=date(2026, 8, 4),
        location="Student Hall",
    )

    bookmark = create_bookmark(event=event, attendee_name="  Ren  ", note="  Bring friends  ")

    assert bookmark.attendee_name == "Ren"
    assert bookmark.note == "Bring friends"


@pytest.mark.django_db
def test_published_events_filters_by_title_category_and_date():
    user = User.objects.create_user(username="sota")
    lecture = Category.objects.create(name="Lecture", slug="lecture")
    sports = Category.objects.create(name="Sports", slug="sports")
    matching = Event.objects.create(
        author=user,
        category=lecture,
        title="Web security lecture",
        description="Security basics",
        date=date(2026, 8, 5),
        location="Room M2",
    )
    Event.objects.create(
        author=user,
        category=sports,
        title="Basketball practice",
        description="Practice",
        date=date(2026, 8, 6),
        location="Gym",
    )

    events = published_events(
        EventFilters(query="security", category_id=lecture.id, date_from=date(2026, 8, 1))
    )

    assert list(events) == [matching]


@pytest.mark.django_db
def test_seed_demo_content_is_idempotent():
    seed_demo_content()
    seed_demo_content()

    assert User.objects.count() == 3
    assert Category.objects.count() == 5
    assert Event.objects.count() == 10


@pytest.mark.django_db
def test_event_list_view(client):
    seed_demo_content()

    response = client.get(reverse("events:event_list"))

    assert response.status_code == 200
    assert "Event Listings" in response.content.decode()


@pytest.mark.django_db
def test_event_create_view(client):
    user = User.objects.create_user(username="sota")
    category = Category.objects.create(name="Lecture", slug="lecture")

    response = client.post(
        reverse("events:event_create"),
        {
            "author": user.id,
            "category": category.id,
            "title": "Django lecture",
            "description": "Intro session",
            "date": "2026-08-01",
            "location": "Room M1",
            "status": Event.Status.PUBLISHED,
        },
    )

    assert response.status_code == 302
    assert Event.objects.filter(title="Django lecture").exists()


@pytest.mark.django_db
def test_htmx_bookmark_create_returns_partial(client):
    user = User.objects.create_user(username="sota")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Campus meetup",
        description="Meet students",
        date=date(2026, 8, 2),
        location="Cafeteria",
    )

    response = client.post(
        reverse("events:bookmark_create", kwargs={"event_id": event.id}),
        {"attendee_name": "Aoi", "note": "I want to join"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert Bookmark.objects.filter(event=event, attendee_name="Aoi").exists()
    assert "I want to join" in response.content.decode()

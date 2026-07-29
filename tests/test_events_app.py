from datetime import date

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from events_app.forms import SearchForm
from events_app.models import Bookmark, Category, Event, Favorite, OrganizerProfile
from events_app.selectors import EventFilters, published_events
from events_app.services import create_bookmark, create_event, seed_demo_content


@pytest.mark.django_db
def test_create_event_service():
    user = User.objects.create_user(username="sota", password="pass-12345")
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
    user = User.objects.create_user(username="sota", password="pass-12345")
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
    user = User.objects.create_user(username="sota", password="pass-12345")
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
def test_published_events_filters_by_description_or_location():
    user = User.objects.create_user(username="sota", password="pass-12345")
    lecture = Category.objects.create(name="Lecture", slug="lecture")
    Event.objects.create(
        author=user,
        category=lecture,
        title="Morning talk",
        description="Deep dive into databases",
        date=date(2026, 8, 5),
        location="Room M2",
    )
    location_match = Event.objects.create(
        author=user,
        category=lecture,
        title="Evening talk",
        description="General session",
        date=date(2026, 8, 6),
        location="Central Library",
    )

    by_description = published_events(EventFilters(query="databases"))
    by_location = published_events(EventFilters(query="library"))

    assert by_description.count() == 1
    assert list(by_location) == [location_match]


def test_search_form_rejects_inverted_date_range():
    form = SearchForm(data={"date_from": "2026-08-10", "date_to": "2026-08-01"})

    assert not form.is_valid()
    assert "date_to" in form.errors


@pytest.mark.django_db
def test_seed_demo_content_is_idempotent():
    seed_demo_content()
    seed_demo_content()

    assert User.objects.count() == 3
    assert Category.objects.count() == 5
    assert Event.objects.count() == 10
    assert OrganizerProfile.objects.count() == 3
    assert User.objects.get(username="sota").check_password("demo-pass-123")
    assert OrganizerProfile.objects.get(user__username="sota").display_name == "Sota Sato"


@pytest.mark.django_db
def test_event_list_view(client):
    seed_demo_content()

    response = client.get(reverse("events:event_list"))

    assert response.status_code == 200
    assert "Event Listings" in response.content.decode()


@pytest.mark.django_db
def test_draft_event_detail_hidden_from_other_users(client):
    author = User.objects.create_user(username="sota", password="pass-12345")
    other_user = User.objects.create_user(username="mika", password="pass-12345")
    category = Category.objects.create(name="Lecture", slug="lecture")
    draft_event = Event.objects.create(
        author=author,
        category=category,
        title="Private draft",
        description="Draft details",
        date=date(2026, 8, 3),
        location="Room M1",
        status=Event.Status.DRAFT,
    )

    guest_response = client.get(reverse("events:event_detail", kwargs={"event_id": draft_event.id}))
    assert guest_response.status_code == 404

    client.login(username=other_user.username, password="pass-12345")
    other_response = client.get(reverse("events:event_detail", kwargs={"event_id": draft_event.id}))
    assert other_response.status_code == 404


@pytest.mark.django_db
def test_author_can_view_own_draft_on_my_page(client):
    author = User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Lecture", slug="lecture")
    Event.objects.create(
        author=author,
        category=category,
        title="Private draft",
        description="Draft details",
        date=date(2026, 8, 3),
        location="Room M1",
        status=Event.Status.DRAFT,
    )
    Event.objects.create(
        author=author,
        category=category,
        title="Cancelled event",
        description="Cancelled details",
        date=date(2026, 8, 4),
        location="Room M2",
        status=Event.Status.CANCELLED,
    )
    client.login(username="sota", password="pass-12345")

    response = client.get(reverse("events:my_page"))

    body = response.content.decode()
    assert response.status_code == 200
    assert "Private draft" in body
    assert "Cancelled event" in body


@pytest.mark.django_db
def test_event_create_requires_login(client):
    response = client.get(reverse("events:event_create"))

    assert response.status_code == 302
    assert reverse("accounts:login") in response.url


@pytest.mark.django_db
def test_event_create_view(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Lecture", slug="lecture")
    client.login(username="sota", password="pass-12345")

    response = client.post(
        reverse("events:event_create"),
        {
            "category": category.id,
            "title": "Django lecture",
            "description": "Intro session",
            "date": "2026-08-01",
            "location": "Room M1",
            "status": Event.Status.PUBLISHED,
        },
    )

    assert response.status_code == 302
    event = Event.objects.get(title="Django lecture")
    assert event.author == user


@pytest.mark.django_db
def test_event_edit_and_delete_by_author(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Lecture", slug="lecture")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Old title",
        description="Old description",
        date=date(2026, 8, 1),
        location="Room M1",
    )
    client.login(username="sota", password="pass-12345")

    edit_response = client.post(
        reverse("events:event_edit", kwargs={"event_id": event.id}),
        {
            "category": category.id,
            "title": "Updated title",
            "description": "Updated description",
            "date": "2026-08-02",
            "location": "Room M2",
            "status": Event.Status.PUBLISHED,
        },
    )
    event.refresh_from_db()

    assert edit_response.status_code == 302
    assert event.title == "Updated title"

    delete_response = client.post(reverse("events:event_delete", kwargs={"event_id": event.id}))
    assert delete_response.status_code == 302
    assert not Event.objects.filter(pk=event.id).exists()


@pytest.mark.django_db
def test_event_edit_forbidden_for_other_user(client):
    author = User.objects.create_user(username="sota", password="pass-12345")
    User.objects.create_user(username="mika", password="pass-12345")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=author,
        category=category,
        title="Campus meetup",
        description="Meet students",
        date=date(2026, 8, 2),
        location="Cafeteria",
    )
    client.login(username="mika", password="pass-12345")

    response = client.get(reverse("events:event_edit", kwargs={"event_id": event.id}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_register_and_login(client):
    register_response = client.post(
        reverse("accounts:register"),
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strong-pass-123",
            "password2": "strong-pass-123",
        },
    )

    assert register_response.status_code == 302
    assert User.objects.filter(username="newuser").exists()

    client.logout()
    login_response = client.post(
        reverse("accounts:login"),
        {"username": "newuser", "password": "strong-pass-123"},
    )

    assert login_response.status_code == 302
    assert login_response.url == reverse("events:event_list")


@pytest.mark.django_db
def test_account_settings_updates_user_and_profile(client):
    user = User.objects.create_user(
        username="sota",
        email="old@example.com",
        password="pass-12345",
    )
    OrganizerProfile.objects.create(
        user=user,
        display_name="Old Name",
        contact_email="old-contact@example.com",
    )
    client.login(username="sota", password="pass-12345")

    response = client.post(
        reverse("accounts:settings"),
        {
            "username": "sota-new",
            "email": "new@example.com",
            "display_name": "Sota Sato",
            "contact_email": "contact@example.com",
            "bio": "I organize web and design events.",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("events:my_page")
    assert user.username == "sota-new"
    assert user.email == "new@example.com"
    assert user.organizer_profile.display_name == "Sota Sato"
    assert user.organizer_profile.contact_email == "contact@example.com"
    assert user.organizer_profile.bio == "I organize web and design events."


@pytest.mark.django_db
def test_password_change_updates_password(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
    client.login(username="sota", password="pass-12345")

    response = client.post(
        reverse("accounts:password_change"),
        {
            "old_password": "pass-12345",
            "new_password1": "new-strong-pass-123",
            "new_password2": "new-strong-pass-123",
        },
    )

    user.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse("events:my_page")
    assert user.check_password("new-strong-pass-123")


@pytest.mark.django_db
@override_settings(MEDIA_ROOT="/tmp/event-listings-test-media")
def test_event_create_view_accepts_poster_upload(client):
    User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Lecture", slug="lecture")
    client.login(username="sota", password="pass-12345")
    poster = SimpleUploadedFile("poster.png", b"fake-image-bytes", content_type="image/png")

    response = client.post(
        reverse("events:event_create"),
        {
            "category": category.id,
            "title": "Poster event",
            "description": "Poster upload event.",
            "date": "2026-08-01",
            "location": "Room M1",
            "status": Event.Status.PUBLISHED,
            "poster": poster,
        },
    )

    event = Event.objects.get(title="Poster event")
    assert response.status_code == 302
    assert bool(event.poster)


@pytest.mark.django_db
def test_bookmark_create_requires_login(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
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
    )

    assert response.status_code == 302
    assert reverse("accounts:login") in response.url
    assert not Bookmark.objects.filter(event=event).exists()


@pytest.mark.django_db
def test_favorite_toggle_requires_login(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Campus meetup",
        description="Meet students",
        date=date(2026, 8, 2),
        location="Cafeteria",
        status=Event.Status.PUBLISHED,
    )

    response = client.post(reverse("events:favorite_toggle", kwargs={"event_id": event.id}))

    assert response.status_code == 302
    assert reverse("accounts:login") in response.url
    assert not Favorite.objects.filter(event=event).exists()


@pytest.mark.django_db
def test_favorite_toggle_adds_and_removes_event(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Campus meetup",
        description="Meet students",
        date=date(2026, 8, 2),
        location="Cafeteria",
        status=Event.Status.PUBLISHED,
    )
    client.login(username="sota", password="pass-12345")

    add_response = client.post(reverse("events:favorite_toggle", kwargs={"event_id": event.id}))
    remove_response = client.post(reverse("events:favorite_toggle", kwargs={"event_id": event.id}))

    assert add_response.status_code == 302
    assert remove_response.status_code == 302
    assert Favorite.objects.filter(user=user, event=event).count() == 0


@pytest.mark.django_db
def test_my_page_shows_favorite_events(client):
    owner = User.objects.create_user(username="sota", password="pass-12345")
    author = User.objects.create_user(username="mika", password="pass-12345")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=author,
        category=category,
        title="Saved event",
        description="Useful event",
        date=date(2026, 8, 2),
        location="Cafeteria",
        status=Event.Status.PUBLISHED,
    )
    Favorite.objects.create(user=owner, event=event)
    client.login(username="sota", password="pass-12345")

    response = client.get(reverse("events:my_page"))

    assert response.status_code == 200
    assert "Saved event" in response.content.decode()


@pytest.mark.django_db
def test_htmx_bookmark_create_returns_partial(client):
    user = User.objects.create_user(username="sota", password="pass-12345")
    category = Category.objects.create(name="Meetup", slug="meetup")
    event = Event.objects.create(
        author=user,
        category=category,
        title="Campus meetup",
        description="Meet students",
        date=date(2026, 8, 2),
        location="Cafeteria",
    )
    client.login(username="sota", password="pass-12345")

    response = client.post(
        reverse("events:bookmark_create", kwargs={"event_id": event.id}),
        {"attendee_name": "Aoi", "note": "I want to join"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert Bookmark.objects.filter(event=event, attendee_name="Aoi").exists()
    assert "I want to join" in response.content.decode()


@pytest.mark.django_db
def test_htmx_event_list_returns_partial(client):
    seed_demo_content()

    response = client.get(
        reverse("events:event_list"),
        {"q": "lecture"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    body = response.content.decode()
    assert "Django intro lecture" in body
    assert "<html" not in body.lower()

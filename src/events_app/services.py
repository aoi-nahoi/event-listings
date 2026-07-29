from __future__ import annotations

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import transaction

from .models import Bookmark, Category, Event, Favorite, OrganizerProfile


@transaction.atomic
def create_event(
    *,
    author: User,
    category: Category,
    title: str,
    description: str,
    date: date,
    location: str,
    status: str,
    poster=None,
) -> Event:
    return Event.objects.create(
        author=author,
        category=category,
        title=title.strip(),
        description=description.strip(),
        poster=poster,
        date=date,
        location=location.strip(),
        status=status,
    )


@transaction.atomic
def update_event(
    *,
    event: Event,
    category: Category,
    title: str,
    description: str,
    date: date,
    location: str,
    status: str,
    poster=None,
) -> Event:
    event.category = category
    event.title = title.strip()
    event.description = description.strip()
    if poster is not None:
        event.poster = poster
    event.date = date
    event.location = location.strip()
    event.status = status
    event.save()
    return event


@transaction.atomic
def delete_event(*, event: Event) -> None:
    event.delete()


@transaction.atomic
def create_bookmark(*, event: Event, attendee_name: str, note: str = "") -> Bookmark:
    return Bookmark.objects.create(
        event=event,
        attendee_name=attendee_name.strip(),
        note=note.strip(),
    )


@transaction.atomic
def toggle_favorite(*, user: User, event: Event) -> bool:
    favorite = Favorite.objects.filter(user=user, event=event).first()
    if favorite is not None:
        favorite.delete()
        return False
    Favorite.objects.create(user=user, event=event)
    return True


@transaction.atomic
def seed_demo_content() -> None:
    if not (User.objects.exists() or Category.objects.exists() or Event.objects.exists()):
        categories = {
            "Lecture": Category.objects.create(name="Lecture", slug="lecture"),
            "Concert": Category.objects.create(name="Concert", slug="concert"),
            "Workshop": Category.objects.create(name="Workshop", slug="workshop"),
            "Sports": Category.objects.create(name="Sports", slug="sports"),
            "Meetup": Category.objects.create(name="Meetup", slug="meetup"),
        }
        users = [
            User.objects.create_user(
                username="sota", email="sota@example.com", password="demo-pass-123"
            ),
            User.objects.create_user(
                username="mika", email="mika@example.com", password="demo-pass-123"
            ),
            User.objects.create_user(
                username="ren", email="ren@example.com", password="demo-pass-123"
            ),
        ]
        profiles = {
            "sota": ("Sota Sato", "sota@example.com"),
            "mika": ("Mika Mori", "mika@example.com"),
            "ren": ("Ren Arai", "ren@example.com"),
        }
        for user in users:
            display_name, contact_email = profiles[user.username]
            OrganizerProfile.objects.get_or_create(
                user=user,
                defaults={"display_name": display_name, "contact_email": contact_email},
            )
        today = date.today()
        samples = [
            ("Django intro lecture", "Lecture", 1, "Room M1"),
            ("Campus acoustic night", "Concert", 2, "Student Hall"),
            ("Portfolio workshop", "Workshop", 3, "Lab 4"),
            ("Morning futsal meetup", "Sports", 4, "Gym"),
            ("International student meetup", "Meetup", 5, "Cafeteria"),
            ("Web security lecture", "Lecture", 6, "Room M2"),
            ("Jazz club concert", "Concert", 8, "Auditorium"),
            ("Resume writing workshop", "Workshop", 9, "Career Center"),
            ("Basketball practice", "Sports", 10, "Gym"),
            ("Programming study meetup", "Meetup", 11, "Library"),
        ]
        for index, (title, category_name, offset, location) in enumerate(samples):
            Event.objects.create(
                author=users[index % len(users)],
                category=categories[category_name],
                title=title,
                description=(
                    "This demo event is used to show event browsing, searching, "
                    "category filtering, date filtering, detail pages, and bookmarks."
                ),
                date=today + timedelta(days=offset),
                location=location,
                status=Event.Status.PUBLISHED,
            )

    profiles = {
        "sota": ("Sota Sato", "sota@example.com"),
        "mika": ("Mika Mori", "mika@example.com"),
        "ren": ("Ren Arai", "ren@example.com"),
    }
    for username, (display_name, contact_email) in profiles.items():
        user = User.objects.filter(username=username).first()
        if user is not None:
            user.set_password("demo-pass-123")
            user.save(update_fields=["password"])
            OrganizerProfile.objects.get_or_create(
                user=user,
                defaults={"display_name": display_name, "contact_email": contact_email},
            )

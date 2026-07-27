from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from django.contrib.auth.models import User
from django.db.models import Count, Q, QuerySet

from .models import Category, Event


@dataclass(frozen=True)
class EventFilters:
    query: str = ""
    category_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None


def published_events(filters: EventFilters | None = None) -> QuerySet[Event]:
    events = Event.objects.select_related(
        "author", "author__organizer_profile", "category"
    ).filter(status=Event.Status.PUBLISHED)
    if not filters:
        return events
    if filters.query:
        events = events.filter(
            Q(title__icontains=filters.query)
            | Q(description__icontains=filters.query)
            | Q(location__icontains=filters.query)
        )
    if filters.category_id:
        events = events.filter(category_id=filters.category_id)
    if filters.date_from:
        events = events.filter(date__gte=filters.date_from)
    if filters.date_to:
        events = events.filter(date__lte=filters.date_to)
    return events


def category_overview() -> QuerySet[Category]:
    return Category.objects.annotate(event_count=Count("events")).order_by("name")


def organizer_overview() -> QuerySet[User]:
    return User.objects.annotate(event_count=Count("events")).order_by("username")

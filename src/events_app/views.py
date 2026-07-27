from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookmarkForm, EventForm, SearchForm
from .models import Event
from .selectors import EventFilters, category_overview, organizer_overview, published_events
from .services import (
    create_bookmark,
    create_event,
    delete_event,
    seed_demo_content,
    update_event,
)


def _filters_from_request(request: HttpRequest) -> EventFilters:
    form = SearchForm(request.GET or None)
    form.is_valid()
    cleaned = getattr(form, "cleaned_data", {}) or {}
    return EventFilters(
        query=cleaned.get("q") or "",
        category_id=cleaned["category"].id if cleaned.get("category") else None,
        date_from=cleaned.get("date_from"),
        date_to=cleaned.get("date_to"),
    )


def _events_page(request: HttpRequest):
    events = published_events(_filters_from_request(request))
    paginator = Paginator(events, 6)
    return paginator.get_page(request.GET.get("page"))


def _filter_querystring(request: HttpRequest) -> str:
    params = request.GET.copy()
    params.pop("page", None)
    return params.urlencode()


def _user_can_manage_event(user, event: Event) -> bool:
    return user.is_authenticated and (user == event.author or user.is_staff)


def _organizer_name(event: Event) -> str:
    profile = getattr(event.author, "organizer_profile", None)
    if profile and profile.display_name:
        return profile.display_name
    return event.author.username


def event_list_view(request: HttpRequest) -> HttpResponse:
    events = published_events(_filters_from_request(request))
    page_obj = _events_page(request)
    filter_query = _filter_querystring(request)
    if request.htmx:
        return render(
            request,
            "events_app/partials/event_results.html",
            {"page_obj": page_obj, "filter_query": filter_query},
        )
    context = {
        "form": SearchForm(request.GET or None),
        "page_obj": page_obj,
        "categories": category_overview(),
        "organizers": organizer_overview(),
        "total_events": events.count(),
        "bookmark_count": Event.objects.aggregate(total=Count("bookmarks"))["total"],
        "filter_query": filter_query,
    }
    return render(request, "events_app/event_list.html", context)


def event_list_partial(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "events_app/partials/event_results.html",
        {
            "page_obj": _events_page(request),
            "filter_query": _filter_querystring(request),
        },
    )


@login_required
def event_create_view(request: HttpRequest) -> HttpResponse:
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        event = create_event(author=request.user, **form.cleaned_data)
        messages.success(request, "Event created.")
        return redirect(event)
    return render(request, "events_app/event_form.html", {"form": form, "mode": "create"})


def event_detail_view(request: HttpRequest, event_id: int) -> HttpResponse:
    event = get_object_or_404(
        Event.objects.select_related(
            "author", "author__organizer_profile", "category"
        ).prefetch_related("bookmarks"),
        pk=event_id,
    )
    bookmark_initial = {}
    if request.user.is_authenticated:
        bookmark_initial["attendee_name"] = request.user.username
    return render(
        request,
        "events_app/event_detail.html",
        {
            "event": event,
            "form": BookmarkForm(initial=bookmark_initial),
            "can_manage": _user_can_manage_event(request.user, event),
            "organizer_name": _organizer_name(event),
        },
    )


@login_required
def event_edit_view(request: HttpRequest, event_id: int) -> HttpResponse:
    event = get_object_or_404(Event.objects.select_related("author", "category"), pk=event_id)
    if not _user_can_manage_event(request.user, event):
        raise PermissionDenied

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            update_event(event=event, **form.cleaned_data)
            messages.success(request, "Event updated.")
            return redirect(event)
    else:
        form = EventForm(
            initial={
                "category": event.category_id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "location": event.location,
                "status": event.status,
            }
        )
    return render(
        request,
        "events_app/event_form.html",
        {"form": form, "mode": "edit", "event": event},
    )


@login_required
def event_delete_view(request: HttpRequest, event_id: int) -> HttpResponse:
    event = get_object_or_404(Event.objects.select_related("author"), pk=event_id)
    if not _user_can_manage_event(request.user, event):
        raise PermissionDenied

    if request.method == "POST":
        delete_event(event=event)
        messages.success(request, "Event deleted.")
        return redirect("events:event_list")
    return render(request, "events_app/event_confirm_delete.html", {"event": event})


@login_required
def bookmark_create_view(request: HttpRequest, event_id: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=event_id)
    form = BookmarkForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        create_bookmark(event=event, **form.cleaned_data)
        messages.success(request, "Event bookmarked.")
        if request.htmx:
            event = Event.objects.prefetch_related("bookmarks").get(pk=event.pk)
            return render(request, "events_app/partials/bookmark_list.html", {"event": event})
        return redirect(event)
    return render(
        request,
        "events_app/event_detail.html",
        {
            "event": event,
            "form": form,
            "can_manage": _user_can_manage_event(request.user, event),
        },
    )


def seed_demo_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        seed_demo_content()
        messages.success(request, "Demo event data is ready.")
    return redirect("events:event_list")

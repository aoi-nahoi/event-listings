from __future__ import annotations

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookmarkForm, EventForm, SearchForm
from .models import Event
from .selectors import EventFilters, category_overview, organizer_overview, published_events
from .services import create_bookmark, create_event, seed_demo_content


def _filters_from_request(request: HttpRequest) -> EventFilters:
    form = SearchForm(request.GET or None)
    if not form.is_valid():
        return EventFilters()
    return EventFilters(
        query=form.cleaned_data.get("q") or "",
        category_id=form.cleaned_data["category"].id
        if form.cleaned_data.get("category")
        else None,
        date_from=form.cleaned_data.get("date_from"),
        date_to=form.cleaned_data.get("date_to"),
    )


def _events_page(request: HttpRequest):
    events = published_events(_filters_from_request(request))
    paginator = Paginator(events, 6)
    return paginator.get_page(request.GET.get("page"))


def event_list_view(request: HttpRequest) -> HttpResponse:
    events = published_events(_filters_from_request(request))
    context = {
        "form": SearchForm(request.GET or None),
        "page_obj": _events_page(request),
        "categories": category_overview(),
        "organizers": organizer_overview(),
        "total_events": events.count(),
        "bookmark_count": Event.objects.aggregate(total=Count("bookmarks"))["total"],
    }
    return render(request, "events_app/event_list.html", context)


def event_list_partial(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "events_app/partials/event_results.html",
        {"page_obj": _events_page(request)},
    )


def event_create_view(request: HttpRequest) -> HttpResponse:
    form = EventForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        event = create_event(**form.cleaned_data)
        messages.success(request, "Event created.")
        return redirect(event)
    return render(request, "events_app/event_form.html", {"form": form})


def event_detail_view(request: HttpRequest, event_id: int) -> HttpResponse:
    event = get_object_or_404(
        Event.objects.select_related("author", "category").prefetch_related("bookmarks"),
        pk=event_id,
    )
    return render(request, "events_app/event_detail.html", {"event": event, "form": BookmarkForm()})


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
    return render(request, "events_app/event_detail.html", {"event": event, "form": form})


def seed_demo_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        seed_demo_content()
        messages.success(request, "Demo event data is ready.")
    return redirect("events:event_list")

from __future__ import annotations

from django.contrib import admin

from .models import Bookmark, Category, Event, Favorite, OrganizerProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "contact_email")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "location", "author", "status")
    list_filter = ("status", "category", "date")
    search_fields = ("title", "description", "location", "author__username")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("event", "attendee_name", "created_at")
    search_fields = ("attendee_name", "note", "event__title")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "created_at")
    search_fields = ("user__username", "event__title")

from __future__ import annotations

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="organizer_profile")
    display_name = models.CharField(max_length=80)
    contact_email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["display_name"]

    def __str__(self) -> str:
        return self.display_name


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    title = models.CharField(max_length=140)
    description = models.TextField()
    poster = models.FileField(
        upload_to="event_posters/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp", "gif"])],
    )
    date = models.DateField()
    location = models.CharField(max_length=160)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("events:event_detail", kwargs={"event_id": self.pk})


class Bookmark(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookmarks")
    attendee_name = models.CharField(max_length=80)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"{self.attendee_name} bookmarked {self.event}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_events")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["user", "event"], name="unique_user_favorite_event")
        ]

    def __str__(self) -> str:
        return f"{self.user.username} favorited {self.event}"

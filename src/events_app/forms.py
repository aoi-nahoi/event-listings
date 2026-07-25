from __future__ import annotations

from django import forms
from django.contrib.auth.models import User

from .models import Category, Event


class EventForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.order_by("username"))
    category = forms.ModelChoiceField(queryset=Category.objects.order_by("name"))
    title = forms.CharField(max_length=140)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    location = forms.CharField(max_length=160)
    status = forms.ChoiceField(choices=Event.Status.choices)


class BookmarkForm(forms.Form):
    attendee_name = forms.CharField(max_length=80)
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search title")
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by("name"),
        required=False,
        empty_label="All categories",
    )
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

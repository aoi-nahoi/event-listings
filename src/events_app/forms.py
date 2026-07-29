from __future__ import annotations

from django import forms

from .models import Category, Event


class EventForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by("name"),
        widget=forms.Select(attrs={"class": "field-input"}),
    )
    title = forms.CharField(
        max_length=140,
        widget=forms.TextInput(attrs={"class": "field-input", "placeholder": "Event title"}),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "class": "field-input",
                "placeholder": "What should people know about this event?",
            }
        )
    )
    poster = forms.FileField(
        required=False,
        help_text="Optional poster image: jpg, png, webp, or gif.",
        widget=forms.ClearableFileInput(attrs={"class": "field-input", "accept": "image/*"}),
    )
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "field-input"}))
    location = forms.CharField(
        max_length=160,
        widget=forms.TextInput(
            attrs={"class": "field-input", "placeholder": "Campus room or venue"}
        ),
    )
    status = forms.ChoiceField(
        choices=Event.Status.choices,
        widget=forms.Select(attrs={"class": "field-input"}),
    )

    def clean_title(self) -> str:
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters.")
        return title

    def clean_description(self) -> str:
        description = self.cleaned_data["description"].strip()
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters.")
        return description


class BookmarkForm(forms.Form):
    attendee_name = forms.CharField(
        max_length=80,
        label="Your name",
        widget=forms.TextInput(attrs={"class": "field-input", "placeholder": "Display name"}),
    )
    note = forms.CharField(
        required=False,
        label="Note (optional)",
        widget=forms.Textarea(
            attrs={"rows": 3, "class": "field-input", "placeholder": "Optional reminder"}
        ),
    )

    def clean_attendee_name(self) -> str:
        name = self.cleaned_data["attendee_name"].strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        return name


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "class": "field-input",
                "placeholder": "Title, description, or location",
                "autocomplete": "off",
            }
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by("name"),
        required=False,
        empty_label="All categories",
        widget=forms.Select(attrs={"class": "field-input"}),
    )
    date_from = forms.DateField(
        required=False,
        label="From",
        widget=forms.DateInput(attrs={"type": "date", "class": "field-input"}),
    )
    date_to = forms.DateField(
        required=False,
        label="To",
        widget=forms.DateInput(attrs={"type": "date", "class": "field-input"}),
    )

    def clean(self):
        cleaned = super().clean()
        date_from = cleaned.get("date_from")
        date_to = cleaned.get("date_to")
        if date_from and date_to and date_to < date_from:
            self.add_error("date_to", "End date must be on or after the start date.")
        return cleaned

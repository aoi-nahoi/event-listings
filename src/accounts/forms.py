from __future__ import annotations

from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from events_app.models import OrganizerProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class ProfileSettingsForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    display_name = forms.CharField(max_length=80, required=False)
    contact_email = forms.EmailField(required=False)
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "field-input",
                "placeholder": "Tell people what kind of events you organize.",
            }
        ),
    )

    def __init__(self, *args, user: User, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        profile, _ = OrganizerProfile.objects.get_or_create(
            user=user,
            defaults={
                "display_name": user.username,
                "contact_email": user.email,
            },
        )
        self.fields["username"].initial = user.username
        self.fields["email"].initial = user.email
        self.fields["display_name"].initial = profile.display_name
        self.fields["contact_email"].initial = profile.contact_email
        self.fields["bio"].initial = profile.bio

    def clean_username(self) -> str:
        username = self.cleaned_data["username"].strip()
        conflict = User.objects.exclude(pk=self.user.pk).filter(username=username).exists()
        if conflict:
            raise forms.ValidationError("This username is already in use.")
        return username

    def save(self) -> User:
        profile = self.user.organizer_profile
        self.user.username = self.cleaned_data["username"]
        self.user.email = self.cleaned_data["email"]
        self.user.save(update_fields=["username", "email"])
        profile.display_name = self.cleaned_data["display_name"].strip() or self.user.username
        profile.contact_email = self.cleaned_data["contact_email"]
        profile.bio = self.cleaned_data["bio"].strip()
        profile.save(update_fields=["display_name", "contact_email", "bio"])
        return self.user


class AccountPasswordChangeForm(PasswordChangeForm):
    pass

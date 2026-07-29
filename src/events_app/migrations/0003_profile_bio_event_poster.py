import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events_app", "0002_favorite"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="poster",
            field=models.FileField(
                blank=True,
                upload_to="event_posters/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "webp", "gif"]
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="organizerprofile",
            name="bio",
            field=models.TextField(blank=True),
        ),
    ]

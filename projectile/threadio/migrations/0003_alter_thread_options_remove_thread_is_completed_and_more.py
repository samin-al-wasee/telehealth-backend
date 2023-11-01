# Generated by Django 4.2.1 on 2023-09-26 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("threadio", "0002_alter_inbox_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="thread",
            options={"ordering": ("-created_at",)},
        ),
        migrations.RemoveField(
            model_name="thread",
            name="is_completed",
        ),
        migrations.RemoveField(
            model_name="thread",
            name="participants",
        ),
        migrations.AddField(
            model_name="thread",
            name="participant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

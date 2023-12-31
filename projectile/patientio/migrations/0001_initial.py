# Generated by Django 4.2.1 on 2023-08-21 13:02

import autoslug.fields
import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import patientio.utils
import phonenumber_field.modelfields
import simple_history.models
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("addressio", "0002_addressconnector_address"),
        ("accountio", "0002_affiliation_organization_descendant_child_and_more"),
        ("doctorio", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "serial_number",
                    models.PositiveIntegerField(editable=False, unique=True),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=patientio.utils.get_patient_slug,
                        unique=True,
                    ),
                ),
                (
                    "image",
                    versatileimagefield.fields.VersatileImageField(
                        blank=True,
                        null=True,
                        upload_to=patientio.utils.get_patient_image_file_path,
                    ),
                ),
                (
                    "secondary_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("secondary_email", models.EmailField(blank=True, max_length=254)),
                (
                    "emergency_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("emergency_email", models.EmailField(blank=True, max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("PAUSED", "Paused"),
                            ("REMOVED", "Removed"),
                        ],
                        default="ACTIVE",
                        max_length=50,
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="addressio.address",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accountio.organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="PrimaryDisease",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=400)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="RelativePatient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "patient_relation",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                ("height", models.FloatField(blank=True, null=True)),
                ("weight", models.IntegerField(blank=True, null=True)),
                ("age", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "blood_group",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NOT_SET", "Not Set"),
                            ("A+", "A Positive"),
                            ("A-", "A Negative"),
                            ("B+", "B Positive"),
                            ("B-", "B Negative"),
                            ("AB+", "Ab Positive"),
                            ("AB-", "Ab Negative"),
                            ("O+", "O Positive"),
                            ("O-", "O Negative"),
                        ],
                        default="NOT_SET",
                        max_length=10,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patientio.patient",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="MedicalHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=300)),
                ("description", models.CharField(max_length=600)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="doctorio.doctor",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accountio.organization",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="patientio.patient",
                    ),
                ),
                (
                    "relative_patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="patientio.relativepatient",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalPatient",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "uid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("created_at", models.DateTimeField(blank=True, editable=False)),
                ("updated_at", models.DateTimeField(blank=True, editable=False)),
                (
                    "serial_number",
                    models.PositiveIntegerField(db_index=True, editable=False),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from=patientio.utils.get_patient_slug
                    ),
                ),
                ("image", models.TextField(blank=True, max_length=100, null=True)),
                (
                    "secondary_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("secondary_email", models.EmailField(blank=True, max_length=254)),
                (
                    "emergency_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None
                    ),
                ),
                ("emergency_email", models.EmailField(blank=True, max_length=254)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("PAUSED", "Paused"),
                            ("REMOVED", "Removed"),
                        ],
                        default="ACTIVE",
                        max_length=50,
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="addressio.address",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="accountio.organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical patient",
                "verbose_name_plural": "historical patients",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddConstraint(
            model_name="patient",
            constraint=models.UniqueConstraint(
                fields=("user", "organization"), name="Organization patient"
            ),
        ),
    ]

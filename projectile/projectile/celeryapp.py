import os, dotenv, logging

from celery import Celery

# Load .env variables
dotenv.read_dotenv()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectile.settings")

app = Celery("projectile")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "appointment_started_notification_for_patient_and_doctor": {
        "task": "notificationio.tasks.create_appointment_start_notification_for_patient_and_doctor",
        "schedule": 30.0,
    },
    "patient_appointment_notification_remainder": {
        "task": "notificationio.tasks.create_appointment_remainder_notification_for_patient",
        "schedule": 30.0,
    },
    "doctor_appointment_remainder_notification": {
        "task": "notificationio.tasks.create_appointment_remainder_notification_for_doctor",
        "schedule": 30.0,
    },
}

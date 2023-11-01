import random
import uuid

# Slug Generators


def get_appointment_slug(instance):
    return f"{instance.patient.user.get_name()}-{instance.organization.name}-{random.randint(111, 999)}"


def get_schedule_slug(instance):
    return f"{instance.date}-{instance.time}"

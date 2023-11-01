import uuid


# Slug Generators
def get_doctor_slug(instance):
    return f"{instance.name}-{instance.organization.name}"


def get_schedule_slug(instance):
    return f"{instance.date}-{instance.time}"


def get_doctor_media_path_prefix(instance, filename):
    return f"doctors/{instance.slug}/{filename}"

import uuid


# Slug Generators
def get_organization_slug(instance):
    return f"{instance.name}"


# Media File Prefixes
def get_organization_media_path_prefix(instance, filename):
    return f"organizations/{instance.slug}/{filename}"


def get_clinic_file_path_prefix(instance, filename):
    prefix = str(uuid.uuid4()).split("-")[:1]
    return f"clinics/{instance.slug}/{prefix}-{filename}"

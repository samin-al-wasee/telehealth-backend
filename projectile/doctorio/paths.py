def get_file_path(instance, filename):
    return f"{instance.clinic.slug}/files/{instance.uid}/{filename}"

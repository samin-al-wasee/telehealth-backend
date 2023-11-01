import random


# Slug Generators
def get_patient_slug(instance):
    return instance.user.get_name()


def get_patient_image_file_path(instance, filename):
    return f"patient/{instance.slug}/{filename}"

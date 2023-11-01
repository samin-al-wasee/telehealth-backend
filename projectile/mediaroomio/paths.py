# Method for getting media image path


def get_mediaimage_image_path(instance, filename):
    return f"mediaimages/{instance.uid}/{filename}"

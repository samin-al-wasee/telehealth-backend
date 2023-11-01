# slug generator


def get_address_slug(instance):
    return instance.country if instance.city else instance.zip_code

def get_notification_slug(instance):
    return f"{instance.organization.name}-{instance.organization.slug}"


def mark_all_as_read(instance):
    return instance.update(is_unread=False)

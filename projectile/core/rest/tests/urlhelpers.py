from django.urls import reverse


def me_detail_url():
    return reverse("me.detail")


def user_patient_url():
    return reverse("patient-register")


def notification_list_url():
    return reverse("notification.list")


def notification_detail_url(notification_uid):
    return reverse("notification.detail", args=[notification_uid])

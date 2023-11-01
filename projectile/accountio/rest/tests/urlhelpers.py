from django.urls import reverse


def public_organization_list_url():
    return reverse("organization.list")

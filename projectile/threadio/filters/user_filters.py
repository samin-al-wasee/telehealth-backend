import django_filters

from threadio.models import Thread


class ThreadFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(
        field_name="participant__type", lookup_expr="exact"
    )

    class Meta:
        model = Thread
        fields = ["user"]

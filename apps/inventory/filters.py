from django_filters import FilterSet, OrderingFilter
from django_filters import filters

from apps.inventory.models import Mobile


class MobileFilter(FilterSet):
    o = OrderingFilter(
        fields=(
            ("available", "is_available"),
            ("created", "created_at"),
        ),
    )
    brand = filters.CharFilter(field_name="brand__title", lookup_expr="icontains")

    class Meta:
        model = Mobile
        fields = []

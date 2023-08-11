from collections import OrderedDict

from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination

from core.http import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "page_size"


class TimeEntriesPagination(CustomPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.qs = queryset
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("total_time", self.qs.aggregate(total_time=Sum("duration"))["total_time"] or 0),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )

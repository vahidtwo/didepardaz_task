from collections import OrderedDict

from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination

from core.http import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "page_size"

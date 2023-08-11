from django.db.models import QuerySet, F
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from apps.inventory.filters import MobileFilter
from apps.inventory.forms import MobileForm
from apps.inventory.models import Mobile
from apps.inventory.serializer import MobileSerializer
from core.views import BaseView


def create_mobile(request):
    """
    View for creating a new mobile.

    For GET requests, displays a form for creating a new mobile.
    For POST requests, processes the form and saves a new mobile.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: Redirects to the list view after successful creation or displays the form again on errors.
    """
    if request.method == "POST":
        form = MobileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_mobiles")  # Redirect to the list view after successful creation
    else:
        form = MobileForm()
    return render(request, "mobile/mobile_form.html", {"form": form})


def list_mobiles(request):
    """
    View for listing mobiles.

    Retrieves all mobile objects and displays them in a list.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: Renders the list view with the retrieved mobiles.
    """
    mobiles = Mobile.objects.all().select_related("brand")  # Retrieve all mobile objects
    return render(request, "mobile/list.html", {"mobiles": mobiles})


def edit_mobile(request, id):
    """
    View for editing a mobile.

    For GET requests, displays a form for editing an existing mobile.
    For POST requests, processes the form and saves the changes to the mobile.

    Args:
        request (HttpRequest): The incoming HTTP request object.
        id (int): The ID of the mobile to be edited.

    Returns:
        HttpResponse: Redirects to the list view after successful edit or displays the form again on errors.
    """
    mobile = get_object_or_404(Mobile, id=id)

    if request.method == "POST":
        form = MobileForm(request.POST, instance=mobile)
        if form.is_valid():
            form.save()
            return redirect("list_mobiles")  # Redirect to the list view after successful edit
    else:
        form = MobileForm(instance=mobile)

    return render(request, "mobile/edit.html", {"form": form, "mobile": mobile})


class MobileReportView(BaseView):
    """
    View for generating mobile reports.

    This view extends a base view and includes filtering capabilities for generating mobile reports.

    Attributes:
        serializer_class (MobileSerializer): The serializer class for mobiles.
        filter_backends (list): The backend classes for filtering.
        filterset_class (MobileFilter): The filter class for mobiles.

    Methods:
        get_queryset(): Retrieves the queryset for generating mobile reports.
        korean_mobiles(request, *args, **kwargs): Lists Korean mobiles.
        same_nationality_and_producer_country(request, *args, **kwargs): Lists mobiles with the same nationality and producer country.
    """

    serializer_class = MobileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MobileFilter

    def get_queryset(self) -> QuerySet[Mobile]:
        """
        Retrieves the queryset for generating mobile reports.

        Returns:
            QuerySet[Mobile]: The filtered queryset for generating reports.
        """
        qs = Mobile.objects.all().select_related("brand__nationality", "producer_country")
        if self.action == "korean_mobiles":
            qs = qs.filter(brand__nationality__title__exact="Korea")
        if self.action == "same_nationality_and_producer_country":
            qs = qs.filter(producer_country=F("brand__nationality"))
        return qs

    def korean_mobiles(self, request, *args, **kwargs):
        """Lists Korean mobiles"""
        return super().list(request, *args, **kwargs)

    def same_nationality_and_producer_country(self, request, *args, **kwargs):
        """Lists mobiles with the same nationality and producer country."""
        return super().list(request, *args, **kwargs)

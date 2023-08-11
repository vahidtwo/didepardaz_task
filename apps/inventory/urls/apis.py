from django.urls import path

from apps.inventory.views import MobileReportView

urlpatterns = [
    path("korean/", MobileReportView.as_view({"get": "korean_mobiles"}), name="korean_mobiles"),
    path(
        "same-country/",
        MobileReportView.as_view({"get": "same_nationality_and_producer_country"}),
        name="same-county-mobiles",
    ),
    path("", MobileReportView.as_view({"get": "list"})),
]

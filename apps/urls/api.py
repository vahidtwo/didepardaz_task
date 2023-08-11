from django.urls import path, include


urlpatterns = [
    path("inventory/", include("apps.inventory.urls.apis")),
]

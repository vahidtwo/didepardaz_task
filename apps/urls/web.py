from django.urls import path, include

urlpatterns = [
    path("mobile/", include("apps.inventory.urls.web")),
]

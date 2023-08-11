from django.urls import path

from apps.inventory import views

urlpatterns = [
    path("add/", views.create_mobile, name="add_mobile"),
    path("", views.list_mobiles, name="list_mobiles"),
    path("edit/<int:id>/", views.edit_mobile, name="edit_mobile"),
]

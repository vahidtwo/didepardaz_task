from django.contrib import admin

from apps.inventory.models import Mobile, Brand
from core.admin.base import BaseAdmin


# Register your models here.
@admin.register(Mobile)
class MobileAdmin(BaseAdmin):
    list_display = ("model", "color_name", "brand")


@admin.register(Brand)
class BrandAdmin(BaseAdmin):
    list_display = ("title", "nationality")

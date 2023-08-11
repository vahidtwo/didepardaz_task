from django.contrib import admin

from apps.location.models import Country


# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("title", "code_name")

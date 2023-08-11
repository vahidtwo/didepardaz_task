from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.admin.base import BaseAdmin
from . import models
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    AdminPasswordChangeForm,
    UsernameField,
    UserChangeForm as DjangoUserChangeForm,
)
from rest_framework.authtoken.models import TokenProxy
admin.site.unregister(TokenProxy)


class UserChangeForm(DjangoUserChangeForm):
    class Meta(DjangoUserChangeForm.Meta):
        pass

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        fields = ("email",)



@admin.register(models.User)
class UserAdmin(UserAdmin, BaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("id", "full_name", "email", "is_staff")
    search_fields = ("email",)
    list_filter = ("first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = tuple()
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "is_staff",
                    "password",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "is_staff",
                )
            },
        ),
    )
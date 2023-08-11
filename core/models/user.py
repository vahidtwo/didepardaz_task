from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser as DjangoAbstractUser
from django.utils.translation import gettext_lazy as _

from core.managers import UserManager
from .base import BaseModel


class AbstractUser(BaseModel, DjangoAbstractUser):
    objects = UserManager()
    is_active = models.BooleanField(  # duplicate name `is_active` in BaseModel and DjangoUserAdmin
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )

    class Meta:
        abstract = True

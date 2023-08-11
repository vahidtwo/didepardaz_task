from django.db import models

from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Country(BaseModel):
    title = models.CharField(max_length=80, verbose_name=_("country"))
    code_name = models.CharField(max_length=80, verbose_name=_("code name"))

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

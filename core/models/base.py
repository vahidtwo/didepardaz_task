import jdatetime
from django.core.cache import cache
from django.db import models
from django.forms.utils import to_current_timezone
from django.utils.text import camel_case_to_spaces
from django.utils.translation import gettext_lazy as _

from core.http import get_client_ip


def datetime2jalali(g_date):
    if g_date is None:
        return None

    g_date = to_current_timezone(g_date)
    jdatetime.set_locale("fa_IR")
    return jdatetime.datetime.fromgregorian(datetime=g_date)


class CustomForeignKey(models.ForeignKey):
    """
    Custom ForeginKey
    custom foreginkey for created_by and created_at
    auto set related names
    """

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        related_name = self.remote_field.related_name
        if not cls._meta.abstract and related_name:
            underscore_name = camel_case_to_spaces(cls.__name__).replace(" ", "_")
            self.remote_field.related_name = related_name.format(underscore_name=underscore_name)


class BaseModel(models.Model):
    """
    Base Model
    methods:
        - jalali_created_at: returns jalali format of created_at attr
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    is_active = models.BooleanField(verbose_name=_("is active"), default=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, "title"):
            return str(self.title)

        return "%s (%s)" % (self._meta.verbose_name, self.id)

    def jalali_created_at(self):
        """
        returns jalali format of created_at attr
        """
        return datetime2jalali(self.created_at)

    jalali_created_at.short_description = _("created_at")

    jalali_created_at = property(jalali_created_at)

    @property
    def seo_object(self):
        if hasattr(self, "seo"):
            return self.seo.last()

    @property
    def formated_jalali_date(self):
        return self.jalali_created_at.strftime("%d %b %Y")

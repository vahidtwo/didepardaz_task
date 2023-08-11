from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from core.models.user import AbstractUser


class User(AbstractUser):
    """User model
    """


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


    @cached_property
    def full_name(self):
        return self.get_full_name()

    full_name.short_description = _("full name")

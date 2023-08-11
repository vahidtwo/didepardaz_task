from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_number_regex_validator = RegexValidator(regex=r"^09\d{9}$", message=_("invalid phone number format"))


egnlish_text_validator = RegexValidator(regex=r"^\w+$", message=_("please enter latin words"))

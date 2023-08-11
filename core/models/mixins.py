import random
import string
from django.db import models
from django.core.cache import cache
from django.utils.crypto import get_random_string
from core.randomization import generate_slug as generate_slug_util
from django.utils.translation import gettext_lazy as _


def generate_slug(obj, title, recersion=False):
    slug = str(title)

    if recersion:
        if not slug.endswith("-"):
            slug += "-"

        rand_char = random.choice(string.digits)
        slug += rand_char

    Model = obj._meta.model
    if Model.objects.filter(slug=slug).exists():
        return generate_slug(obj, slug, recersion=True)

    slug = slug.replace(" ", "-")
    return slug


class SlugMixin(models.Model):
    slug = models.CharField(max_length=200, verbose_name=_("slug"))

    def set_slug(self):
        if hasattr(self, "title"):
            self.slug = generate_slug(self, self.title)
        else:
            self.slug = generate_slug_util()
        self.save()
        return self.slug

    class Meta:
        abstract = True


class IconMixin(models.Model):
    icon = models.ImageField(upload_to="icons/", null=True, blank=True)

    class Meta:
        abstract = True


# Account Mixins
class OTPMixin(models.Model):
    """
    OTP Mixin Model
    methods
        - set_otp: generate random otp in `otp_length` conf length store hashed otp in memcache
            returns real otp digits
        - check_otp: check otp value with hashed otp in memcache
    """

    otp_length = 5

    class Meta:
        abstract = True

    @property
    def __key(self):
        return "otp_%s" % self.pk

    def set_otp(self):
        """
        Set Otp Method
        returns Otp in digits format`
        """
        length = self.otp_length
        otp = get_random_string(length=length, allowed_chars=string.digits)
        # value = make_password(otp)
        # changed otp from hash value to real value
        # we should show it in admin panel (i don't know why : |)
        value = otp
        cache.set(self.__key, value, 60 * 4)
        return otp

    def check_otp(self, value):
        """
        Check Otp Method
        returns Bool object
        """
        otp = self.get_otp()
        return otp == value
        # if otp is not None:
        # return check_password(value, otp)
        # return False

    def get_otp(self):
        """
        Returns assigned otp value
        """
        return cache.get(self.__key)


class EmailVerifyMixin(models.Model):
    """
    Email Mixin Model
    methods
        - set_code: generate random otp in `code_length` conf length store hashed code in memcache
            returns real otp digits
        - check_code: check code value with hashed code in memcache
    """

    code_length = 5

    class Meta:
        abstract = True

    @property
    def __key(self):
        return "email_verify_code_%s" % self.pk

    def set_code(self):
        """
        Set code Method
        returns code in digits format`
        """
        length = self.code_length
        code = get_random_string(length=length, allowed_chars=string.digits)
        value = code
        cache.set(self.__key, value, 60 * 30)
        return code

    def check_code(self, value):
        """
        Check code Method
        returns Bool object
        """
        code = self.get_code()
        return code == value

    def get_code(self):
        """
        Returns assigned otp value
        """
        return cache.get(self.__key)

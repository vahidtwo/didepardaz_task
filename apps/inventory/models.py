from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Brand(BaseModel):
    """
    Represents a mobile brand.

    Attributes:
        title (str): The title of the brand.
        nationality (ForeignKey): The nationality of the brand.
    """

    title = models.CharField(max_length=80, verbose_name=_("brand"))
    nationality = models.ForeignKey("location.Country", on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")


class Mobile(BaseModel):
    """
    Represents a mobile device.

    Attributes:
        brand (ForeignKey): The brand of the mobile.
        model (str): The model name of the mobile.
        price (int): The price of the mobile.
        color_name (str): The name of the color.
        color_code (str): The color code in hexadecimal format (e.g., #010232).
        size (Decimal): The size of the mobile.
        producer_country (ForeignKey): The country where the mobile is produced.
        is_available (bool): Whether the mobile is available.

    Meta:
        ordering (tuple): Specifies the default ordering of records.
        unique_together (list): Ensures uniqueness of brand and model together.
        indexes (list): Defines database indexes for optimized querying.
    """

    brand = models.ForeignKey("inventory.Brand", on_delete=models.PROTECT)
    model = models.CharField(max_length=80, verbose_name=_("model name"))
    price = models.PositiveIntegerField(verbose_name=_("price"))
    color_name = models.CharField(max_length=80, verbose_name=_("color name"))
    color_code = models.CharField(
        max_length=9, verbose_name=_("color code"), help_text=_("color code for eg: #010232"), null=True, blank=True
    )
    size = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("size"))
    producer_country = models.ForeignKey(
        "location.Country", on_delete=models.PROTECT, verbose_name=_("producer country")
    )
    is_available = models.BooleanField(verbose_name=_("is available"))

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("mobile")
        verbose_name_plural = _("mobiles")
        unique_together = ["brand", "model"]
        indexes = [models.Index(fields=["model", "is_available"])]

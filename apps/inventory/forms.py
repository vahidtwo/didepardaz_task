from django import forms

from apps.inventory.models import Mobile


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ("brand", "model", "price", "color_name", "color_code", "size", "producer_country", "is_available")

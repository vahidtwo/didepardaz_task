from rest_framework import serializers

from apps.inventory.models import Mobile, Brand


class BrandSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source="nationality.title")

    class Meta:
        model = Brand
        fields = ("title", "nationality")


class MobileSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    producer_country = serializers.CharField(source="producer_country.title")

    class Meta:
        model = Mobile
        fields = ("brand", "model", "price", "color_name", "color_code", "size", "producer_country", "is_available")
        read_only_fields = fields

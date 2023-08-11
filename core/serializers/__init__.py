from rest_framework.serializers import ModelSerializer as DRFModelSerializer
from .abstract_base_serializer import AbstractBaseSerializer


class ModelSerializer(AbstractBaseSerializer, DRFModelSerializer):
    """
    custom model serializer that have some new features:
    1- a model serializer has two new parameter
        - fields: can determine which fields must be used in serializer
            this may use when serializer has 5 fields in meta, and we need 2 of them
        - exclude: can determine which fields removed from fields that write in meta class
    2- changed_fields: a method that return which fields updated during update
    3- a field that return jalali of created_at field
        this field can be used in Meta class
    """

    def build_property_field(self, field_name, model_class):
        return super().build_property_field(field_name, model_class)

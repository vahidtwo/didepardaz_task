from rest_framework import fields


class AbstractBaseSerializer:
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        super().__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude:
            not_allowed = set(exclude)
            for field_name in not_allowed:
                self.fields.pop(field_name)

    def changed_fields(self, changed_data=[]):
        for field, value in self.validated_data.items():
            if value != getattr(self.instance, field, None):
                changed_data.append(field)
        return changed_data

    def build_property_field(self, field_name, model_class):
        if field_name == "jalali_created_at":
            return fields.DateTimeField, {"read_only": True}
        return super().build_property_field(field_name, model_class)

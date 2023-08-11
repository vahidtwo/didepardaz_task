import jalali_date
from rest_framework import serializers


class DateSerializerMixing(serializers.Serializer):
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return jalali_date.datetime2jalali(obj.created_at).strftime("%Y-%m-%d")

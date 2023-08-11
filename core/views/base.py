"""
Views
Contains BaseView support mutilple serializer and permissions per action
Also async update queryset
Author: mehrab <mehrabox@gmail.com>
"""

import asyncio

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings

from . import mixins

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


class BaseModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.ModelViewSet,
):
    pass


class BaseView(BaseModelViewSet):
    """
    BaseView
    Support mutilple serializer and permissions per action
    public methods:
        - async_update_queryset: async update an queryset with given attrs
        - async_update_instance: async update an object wioth given attrs

    serializers
        create an dict of actions in keys and serializer in values
        or you can set an `default` serializer for other actions
        example:
            serializer = {
                "default": DefaultSerializer,
                "cerated": CreatedObjectSerializer,
                ...
            }
            key choices is all ModelViewSet actions
    action_permissions
        create an dict of actions in keys and permission in values
        or you can set an `default` serializer for other actions
        example:
            action_permissions = {
                "default": IsAuthenticated,
                "cerated": [IsAuthenticated, HasPermFoo, HasPermBar], # example list value
                ...
            }
            key choices is all ModelViewSet actions
            Also you can create list of permissions in values
    """

    serializer_class = None
    serializers = {"default": None}
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    action_permissions = {"default": permission_classes[0]}

    lookup_field = "id"

    def get_serializer_class(self) -> Serializer | NotImplementedError:
        if getattr(self, "serializer_class", None):
            return self.serializer_class

        elif hasattr(self, "serializers"):
            return self.serializers.get(self.action, self.serializers.get("default", None))
        else:
            raise NotImplementedError("you should provide `serializer_class` or `serializers` attr")

    def get_permissions(self):
        permissions = self.action_permissions.get(self.action, self.action_permissions.get("default"))
        if hasattr(permissions, "__iter__"):
            return [permission() for permission in permissions]
        else:
            return [permissions()]

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(request, message=getattr(permission, "message", None))

    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request, message=getattr(permission, "message", None))

    def __update_instance(self, *args):
        instance, attrs = args
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        instance.save()

    def __update_queryset(self, *args):
        args = tuple(args[0])
        qs, attrs = args
        if isinstance(qs, QuerySet):
            qs.update(**attrs)
        else:
            for instance in qs:
                self.__update_instance(instance, attrs)

    def async_update_instance(self, instance, attrs):
        args = (instance, attrs)
        return self.__update_instance(instance, attrs)

    def async_update_queryset(self, qs, attrs):
        args = [qs, attrs]
        return loop.run_in_executor(None, self.__update_queryset, args)

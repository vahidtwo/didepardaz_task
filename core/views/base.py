"""
Views
Contains BaseView support mutilple serializer and permissions per action
Also async update queryset
Author: mehrab <mehrabox@gmail.com>
"""

import asyncio

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
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
    for pagination :
        1. pagination_class set it set for all view actions that in pagination_actions
        2. paginate_classes set it retrieve for that view action
        example:
            >>> class MYVIew(BaseView):
            1:
            >>>     paginate_class = SomePaginationClass
            >>>     pagination_actions = ['list', 'some_get_action']
            2:
            >>>     serializer_class = SomePaginationClass
            3:
            >>>     paginate_classes = {'default': SomePaginationClass, 'list': OtherPaginationClass}

            or for set for all view actions
            >>>     paginate_classes = {'default': SomePaginationClass}
            or
            >>>     paginate_class = SomePaginationClass
    lookup_fields a dictionary that defines what lookup-field must return in this action
    """

    serializer_class = None
    serializers = {"default": None}
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    action_permissions = {"default": permission_classes[0]}
    paginate_classes = dict()
    lookup_field = "id"
    pagination_actions = []
    lookup_fields = ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.lookup_fields is ...:
            self.lookup_fields = {"default": self.lookup_field}

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_fields.get(self.action, self.lookup_fields.get("default") or self.lookup_field)

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly." % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {lookup_url_kwarg: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self) -> Serializer | NotImplementedError:
        if getattr(self, "serializer_class", None):
            return self.serializer_class

        elif hasattr(self, "serializers"):
            return self.serializers.get(self.action, self.serializers.get("default", None))
        else:
            raise NotImplementedError("you should provide `serializer_class` or `serializers` attr")

    def get_serializer(self, *args, **kwargs) -> Serializer:
        return super().get_serializer(*args, **kwargs)

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

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
            if pagination_class set it set for all view actions that in pagination_actions
            if paginate_classes set it retrieve for that view action
        """

        if not hasattr(self, "_paginator"):
            assert not (
                self.paginate_classes and self.pagination_actions
            ), "just set one of paginate_classes and pagination_actions"
            if self.pagination_class and self.action in self.pagination_actions:
                self._paginator = self.pagination_class()
            elif self.pagination_class and not self.pagination_actions:
                self._paginator = self.pagination_class()
            else:
                if self.paginate_classes:
                    pagination_class = self.paginate_classes.get(
                        self.action, self.paginate_classes.get("default", None)
                    )
                    self._paginator = pagination_class() if pagination_class else None
                else:
                    self._paginator = None
        return self._paginator

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

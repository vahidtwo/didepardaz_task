from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    exclude = ("is_active",)

    def get_fieldsets(self, request, obj=None):
        if obj is None and hasattr(self, "add_fieldsets"):
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def is_supper_user_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        return self.is_supper_user_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.is_supper_user_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.is_supper_user_permission(request)

    def has_module_permission(self, request):
        return self.has_view_permission(request)

    def has_view_permission(self, request, obj=None):
        if self.is_supper_user_permission(request):
            return True
        return (
            self.has_add_permission(request)
            or self.has_delete_permission(request)
            or self.has_change_permission(request)
        )

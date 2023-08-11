from core.admin.utils import link_image
from django.utils.translation import gettext_lazy as _


class LogoAdminMixing:
    def thumb(self, obj):
        return link_image(obj.logo) if obj.logo else None

    thumb.short_description = _("logo")

    def get_list_display(self, request):
        return self.list_display + ("thumb",)


class IconAdminMixing:
    def thumb(self, obj):
        return link_image(obj.icon) if obj.icon else None

    thumb.short_description = _("icon")

    def get_list_display(self, request):
        return self.list_display + ("thumb",)

from django.contrib import admin
from django.utils.safestring import mark_safe


def custom_titled_filter(title):
    """
    This method change default list_filter admin value
    for use it does somthing like
    list_filter = (('role__title',  custom_titled_filter(_('custom title'))
    @param title:
    @return:
    """

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def link_image(image, url=None, width=50, height=50):
    url = url if url else image.url
    width = 'width="{}"'.format(width)
    height = 'height="{}"'.format(height)
    return mark_safe('<a href="{}"><img src="{}" {} {}/></a>'.format(url, image.url, width, height))

from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html
from adminsortable2.admin import SortableStackedInline, SortableAdminBase


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']

    def image_preview(self, obj):
        return format_html('<img src={} style="max-height: 200px;"/>',
            obj.image.url,
        )

@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    ordering = ['id']
    inlines = [PlaceImageInline]


admin.site.register(PlaceImage)
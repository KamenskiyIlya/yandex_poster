from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Place, PlaceImage
from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from tinymce.widgets import TinyMCE


class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        widgets = {
            'description_long': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']

    def image_preview(self, obj):
        return format_html('<img src={} style="max-height: 200px;" />',
            obj.image.url,
        )

@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    ordering = ['id']
    inlines = [PlaceImageInline]



admin.site.register(PlaceImage)
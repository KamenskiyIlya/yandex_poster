from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from .models import Place, PlaceImage


class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        widgets = {'long_description': TinyMCE(attrs={'cols': 80, 'rows': 30})}


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']

    def image_preview(self, obj):
        return format_html(
            '<img src={} style="max-height: 200px; max-width:300px" />',
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


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['place']

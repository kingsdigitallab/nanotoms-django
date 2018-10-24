from django.contrib import admin
from atoms.models import Item, Location, Media, Source, Text
from polymorphic.admin import (PolymorphicChildModelAdmin,
                               PolymorphicChildModelFilter,
                               PolymorphicParentModelAdmin)


@admin.register(Item)
class ItemAdmin(PolymorphicParentModelAdmin):
    child_models = [Location, Media, Text]
    list_filter = [PolymorphicChildModelFilter]
    search_fields = ['title']


class ItemChildAdmin(PolymorphicChildModelAdmin):
    autocomplete_fields = ['source', 'items']
    list_display = ['title', 'source']
    show_in_index = True


@admin.register(Location)
class LocationAdmin(ItemChildAdmin):
    pass


@admin.register(Media)
class MediaAdmin(ItemChildAdmin):
    pass


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Text)
class TextAdmin(ItemChildAdmin):
    pass

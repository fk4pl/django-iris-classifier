from django.contrib import admin
from .models import IrisSample, Collection


@admin.register(IrisSample)
class IrisSampleAdmin(admin.ModelAdmin):
    list_display = ('instance_id', 'species', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    search_fields = ('instance_id', 'species')
    list_filter = ('species',)
    fieldsets = (
        ('Bilgiler', {
            'fields': ('instance_id', 'species')
        }),
        ('Ölçümler (cm)', {
            'fields': ('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
        }),
    )
    ordering = ('instance_id',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner_name', 'public', 'created_at')
    filter_horizontal = ('samples',)

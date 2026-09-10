from django.contrib import admin
from django.utils.html import format_html
from .models import Buff, Effect, Race, Collection, Card, CardAppliedBuff, CardContainedEffect


@admin.register(Buff)
class BuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'attributes_display', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def attributes_display(self, obj):
        attrs = ', '.join([f"{a['name']}:{a['type']}" for a in obj.attributes])
        return attrs or "—"
    attributes_display.short_description = "Attributes"


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ['name', 'attributes_display', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def attributes_display(self, obj):
        attrs = ', '.join([f"{a['name']}:{a['type']}" for a in obj.attributes])
        return attrs or "—"
    attributes_display.short_description = "Attributes"


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'cards_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def cards_count(self, obj):
        return obj.cards.count()
    cards_count.short_description = "Cards"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'health', 'attack', 'races_display', 'collections_display', 'created_at']
    list_filter = ['level', 'races', 'collections', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    filter_horizontal = ['races', 'collections']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'image_preview')
        }),
        ('Attributes', {
            'fields': ('level', 'races', 'collections', 'attack', 'health')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def races_display(self, obj):
        return ', '.join(r.name for r in obj.races.all()) or "—"
    races_display.short_description = "Races"

    def collections_display(self, obj):
        return ', '.join(c.name for c in obj.collections.all()) or "—"
    collections_display.short_description = "Collections"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Preview"


class CardAppliedBuffInline(admin.TabularInline):
    model = CardAppliedBuff
    extra = 1
    fields = ['buff', 'parameters']


class CardContainedEffectInline(admin.TabularInline):
    model = CardContainedEffect
    extra = 1
    fields = ['effect', 'parameters']


@admin.register(CardAppliedBuff)
class CardAppliedBuffAdmin(admin.ModelAdmin):
    list_display = ['card', 'buff', 'parameters_display', 'created_at']
    list_filter = ['buff', 'created_at']
    search_fields = ['card__title', 'buff__name']
    readonly_fields = ['created_at', 'updated_at']

    def parameters_display(self, obj):
        return str(obj.parameters)[:50]
    parameters_display.short_description = "Parameters"


@admin.register(CardContainedEffect)
class CardContainedEffectAdmin(admin.ModelAdmin):
    list_display = ['card', 'effect', 'parameters_display', 'created_at']
    list_filter = ['effect', 'created_at']
    search_fields = ['card__title', 'effect__name']
    readonly_fields = ['created_at', 'updated_at']

    def parameters_display(self, obj):
        return str(obj.parameters)[:50]
    parameters_display.short_description = "Parameters"

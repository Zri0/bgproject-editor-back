from django.contrib import admin
from django.utils.html import format_html
from .models import Buff, Efecto, Carta, CartaBuffAplicado, CartaEfectoContenido


@admin.register(Buff)
class BuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'atributos_display', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def atributos_display(self, obj):
        attrs = ', '.join([f"{a['nombre']}:{a['tipo']}" for a in obj.atributos])
        return attrs or "—"
    atributos_display.short_description = "Atributos"


@admin.register(Efecto)
class EfectoAdmin(admin.ModelAdmin):
    list_display = ['name', 'atributos_display', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def atributos_display(self, obj):
        attrs = ', '.join([f"{a['nombre']}:{a['tipo']}" for a in obj.atributos])
        return attrs or "—"
    atributos_display.short_description = "Atributos"


@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nivel', 'vida', 'ataque', 'razas_display', 'created_at']
    list_filter = ['nivel', 'created_at']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['created_at', 'updated_at', 'imagen_preview']
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'imagen', 'imagen_preview')
        }),
        ('Atributos', {
            'fields': ('nivel', 'razas', 'ataque', 'vida')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def razas_display(self, obj):
        return ', '.join(obj.razas) if obj.razas else "—"
    razas_display.short_description = "Razas"

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.imagen
            )
        return "—"
    imagen_preview.short_description = "Vista Previa"


class CartaBuffAplicadoInline(admin.TabularInline):
    model = CartaBuffAplicado
    extra = 1
    fields = ['buff', 'parametros']


class CartaEfectoContenidoInline(admin.TabularInline):
    model = CartaEfectoContenido
    extra = 1
    fields = ['efecto', 'parametros']


@admin.register(CartaBuffAplicado)
class CartaBuffAplicadoAdmin(admin.ModelAdmin):
    list_display = ['carta', 'buff', 'parametros_display', 'created_at']
    list_filter = ['buff', 'created_at']
    search_fields = ['carta__titulo', 'buff__name']
    readonly_fields = ['created_at', 'updated_at']

    def parametros_display(self, obj):
        return str(obj.parametros)[:50]
    parametros_display.short_description = "Parámetros"


@admin.register(CartaEfectoContenido)
class CartaEfectoContenidoAdmin(admin.ModelAdmin):
    list_display = ['carta', 'efecto', 'parametros_display', 'created_at']
    list_filter = ['efecto', 'created_at']
    search_fields = ['carta__titulo', 'efecto__name']
    readonly_fields = ['created_at', 'updated_at']

    def parametros_display(self, obj):
        return str(obj.parametros)[:50]
    parametros_display.short_description = "Parámetros"

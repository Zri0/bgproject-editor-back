from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields import JSONField as PostgresJSONField
import json

# Usar JSONField de Django 3.1+ (compatible con SQLite y PostgreSQL)
class JSONField(models.JSONField):
    def get_default(self):
        if callable(self.default):
            return self.default()
        return self.default


class Buff(models.Model):
    """
    Buff: Una mejora que se puede aplicar a una carta.
    Define un conjunto de atributos (nombre-tipo) que son contenedores de valores.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # Atributos: lista de dicts con estructura {"nombre": str, "tipo": str}
    # Ej: [{"nombre": "hp", "tipo": "entero"}, {"nombre": "attack", "tipo": "entero"}]
    atributos = JSONField(default=list, help_text="Lista de atributos con nombre y tipo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Buff"
        verbose_name_plural = "Buffs"
        ordering = ['name']


class Efecto(models.Model):
    """
    Efecto: Una condición/efecto que puede estar contenido en una carta.
    Estructura idéntica a Buff: Define atributos (nombre-tipo).
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # Atributos: lista de dicts con estructura {"nombre": str, "tipo": str}
    atributos = JSONField(default=list, help_text="Lista de atributos con nombre y tipo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Efecto"
        verbose_name_plural = "Efectos"
        ordering = ['name']


class Carta(models.Model):
    """
    Carta: La entidad principal del editor.
    Contiene información base + relaciones a Buffs y Efectos aplicados.
    """
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    imagen = models.URLField(help_text="URL de la imagen de la carta")
    nivel = models.IntegerField()
    # Razas: lista de strings (múltiples razas por carta)
    razas = JSONField(default=list, help_text="Lista de razas (strings)")
    ataque = models.IntegerField()
    vida = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} (Nivel {self.nivel})"

    class Meta:
        verbose_name = "Carta"
        verbose_name_plural = "Cartas"
        ordering = ['-created_at']


class CartaBuffAplicado(models.Model):
    """
    Relación: Buff aplicado a una Carta con sus parámetros específicos.
    Parámetros: dict con clave-valor que cumplen los atributos del Buff.
    Ej: {"hp": 10, "attack": 5} para un Buff con atributos hp:entero, attack:entero
    """
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE, related_name='buffs_aplicados')
    buff = models.ForeignKey(Buff, on_delete=models.CASCADE)
    # Parámetros: dict con valores específicos para esta instancia
    parametros = JSONField(default=dict, help_text="Parámetros específicos del buff en esta carta")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.carta.titulo} -> {self.buff.name}"

    class Meta:
        verbose_name = "Buff Aplicado"
        verbose_name_plural = "Buffs Aplicados"
        unique_together = ('carta', 'buff')


class CartaEfectoContenido(models.Model):
    """
    Relación: Efecto contenido en una Carta con sus parámetros específicos.
    Parámetros: dict con clave-valor que cumplen los atributos del Efecto.
    """
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE, related_name='efectos')
    efecto = models.ForeignKey(Efecto, on_delete=models.CASCADE)
    # Parámetros: dict con valores específicos para esta instancia
    parametros = JSONField(default=dict, help_text="Parámetros específicos del efecto en esta carta")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.carta.titulo} ~ {self.efecto.name}"

    class Meta:
        verbose_name = "Efecto Contenido"
        verbose_name_plural = "Efectos Contenidos"
        unique_together = ('carta', 'efecto')

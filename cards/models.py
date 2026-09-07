from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields import JSONField as PostgresJSONField
import json

# Use Django 3.1+ JSONField (compatible with SQLite and PostgreSQL)
class JSONField(models.JSONField):
    def get_default(self):
        if callable(self.default):
            return self.default()
        return self.default


class Buff(models.Model):
    """
    Buff: An improvement that can be applied to a card.
    Defines a set of attributes (name-type) that are value containers.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # Attributes: list of dicts with structure {"name": str, "type": str}
    # E.g.: [{"name": "hp", "type": "integer"}, {"name": "attack", "type": "integer"}]
    attributes = JSONField(default=list, help_text="List of attributes with name and type")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Buff"
        verbose_name_plural = "Buffs"
        ordering = ['name']


class Effect(models.Model):
    """
    Effect: A condition/effect that can be contained in a card.
    Structure identical to Buff: Defines attributes (name-type).
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # Attributes: list of dicts with structure {"name": str, "type": str}
    attributes = JSONField(default=list, help_text="List of attributes with name and type")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Effect"
        verbose_name_plural = "Effects"
        ordering = ['name']


class Race(models.Model):
    """
    Race: A creature type that can be assigned to one or more Cards.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Race"
        verbose_name_plural = "Races"
        ordering = ['name']


class Card(models.Model):
    """
    Card: The main entity of the editor.
    Contains base information + relationships to applied Buffs and Effects.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='cards/',
        blank=True,
        null=True,
        help_text="Card image file (stored and served by Django)"
    )
    level = models.IntegerField()
    races = models.ManyToManyField(Race, related_name='cards', blank=True, help_text="Races assigned to this card")
    attack = models.IntegerField()
    health = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Level {self.level})"

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        ordering = ['-created_at']


class CardAppliedBuff(models.Model):
    """
    Relationship: Buff applied to a Card with its specific parameters.
    Parameters: key-value dict that satisfies the Buff's attributes.
    E.g.: {"hp": 10, "attack": 5} for a Buff with attributes hp:integer, attack:integer
    """
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='applied_buffs')
    buff = models.ForeignKey(Buff, on_delete=models.CASCADE)
    # Parameters: dict with specific values for this instance
    parameters = JSONField(default=dict, help_text="Specific parameters for this buff on this card")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card.title} -> {self.buff.name}"

    class Meta:
        verbose_name = "Applied Buff"
        verbose_name_plural = "Applied Buffs"
        unique_together = ('card', 'buff')


class CardContainedEffect(models.Model):
    """
    Relationship: Effect contained in a Card with its specific parameters.
    Parameters: key-value dict that satisfies the Effect's attributes.
    """
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='effects')
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
    # Parameters: dict with specific values for this instance
    parameters = JSONField(default=dict, help_text="Specific parameters for this effect on this card")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card.title} ~ {self.effect.name}"

    class Meta:
        verbose_name = "Contained Effect"
        verbose_name_plural = "Contained Effects"
        unique_together = ('card', 'effect')

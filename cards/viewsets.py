from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Buff, Effect, Race, Collection, Card, CardAppliedBuff, CardContainedEffect
from .serializers import (
    BuffSerializer,
    EffectSerializer,
    RaceSerializer,
    CollectionSerializer,
    CardListSerializer,
    CardDetailSerializer,
    CardAppliedBuffSerializer,
    CardContainedEffectSerializer,
)


class BuffViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Buffs.
    Buffs are loaded from configuration and are not edited in the application.
    """
    queryset = Buff.objects.all()
    serializer_class = BuffSerializer


class EffectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Effects.
    Effects are loaded from configuration and are not edited in the application.
    """
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer


class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Races.
    Races are loaded from configuration and are not edited in the application.
    """
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    """
    Full ViewSet for Collection CRUD.
    A Collection is a named group of Cards; a Card can belong to zero,
    one, or many Collections.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    Full ViewSet for Card CRUD.
    Supports:
    - GET /cards/ (list)
    - GET /cards/{id}/ (detail with relationships)
    - POST /cards/ (create)
    - PUT /cards/{id}/ (update)
    - DELETE /cards/{id}/ (delete)
    - POST /cards/{id}/add_buff/ (add buff to card)
    - DELETE /cards/{id}/remove_buff/{buff_id}/ (remove buff)
    - POST /cards/{id}/add_effect/ (add effect to card)
    - DELETE /cards/{id}/remove_effect/{effect_id}/ (remove effect)
    """
    queryset = Card.objects.all().prefetch_related('applied_buffs', 'effects')

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return CardDetailSerializer
        return CardListSerializer

    @action(detail=True, methods=['post'], url_path='add-buff')
    def add_buff(self, request, pk=None):
        """
        Add an applied buff to a card.
        Body: {"buff": <buff_id>, "parameters": {...}}
        """
        card = self.get_object()
        buff_id = request.data.get('buff')
        parameters = request.data.get('parameters', {})

        try:
            buff = Buff.objects.get(id=buff_id)
        except Buff.DoesNotExist:
            return Response(
                {'error': 'Buff not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate that the parameters match the buff's attributes
        buff_attributes = {attr['name']: attr['type'] for attr in buff.attributes}
        for key in parameters.keys():
            if key not in buff_attributes:
                return Response(
                    {'error': f'Parameter "{key}" is not defined in the buff\'s attributes'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create or update the relationship
        applied_buff, created = CardAppliedBuff.objects.update_or_create(
            card=card,
            buff=buff,
            defaults={'parameters': parameters}
        )

        serializer = CardAppliedBuffSerializer(applied_buff)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove-buff/(?P<buff_id>[^/.]+)')
    def remove_buff(self, request, pk=None, buff_id=None):
        """Remove a buff from a card."""
        card = self.get_object()
        try:
            CardAppliedBuff.objects.get(card=card, buff_id=buff_id).delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except CardAppliedBuff.DoesNotExist:
            return Response(
                {'error': 'Buff not applied to this card'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], url_path='add-effect')
    def add_effect(self, request, pk=None):
        """
        Add a contained effect to a card.
        Body: {"effect": <effect_id>, "parameters": {...}}
        """
        card = self.get_object()
        effect_id = request.data.get('effect')
        parameters = request.data.get('parameters', {})

        try:
            effect = Effect.objects.get(id=effect_id)
        except Effect.DoesNotExist:
            return Response(
                {'error': 'Effect not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate that the parameters match the effect's attributes
        effect_attributes = {attr['name']: attr['type'] for attr in effect.attributes}
        for key in parameters.keys():
            if key not in effect_attributes:
                return Response(
                    {'error': f'Parameter "{key}" is not defined in the effect\'s attributes'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create or update the relationship
        contained_effect, created = CardContainedEffect.objects.update_or_create(
            card=card,
            effect=effect,
            defaults={'parameters': parameters}
        )

        serializer = CardContainedEffectSerializer(contained_effect)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove-effect/(?P<effect_id>[^/.]+)')
    def remove_effect(self, request, pk=None, effect_id=None):
        """Remove an effect from a card."""
        card = self.get_object()
        try:
            CardContainedEffect.objects.get(card=card, effect_id=effect_id).delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except CardContainedEffect.DoesNotExist:
            return Response(
                {'error': 'Effect not contained in this card'},
                status=status.HTTP_404_NOT_FOUND
            )

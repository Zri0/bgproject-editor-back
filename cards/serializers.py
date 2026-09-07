from rest_framework import serializers
from .models import Buff, Effect, Race, Card, CardAppliedBuff, CardContainedEffect


class BuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buff
        fields = ['id', 'name', 'description', 'attributes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class EffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = ['id', 'name', 'description', 'attributes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CardAppliedBuffSerializer(serializers.ModelSerializer):
    buff_detail = BuffSerializer(source='buff', read_only=True)

    class Meta:
        model = CardAppliedBuff
        fields = ['id', 'buff', 'buff_detail', 'parameters', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CardContainedEffectSerializer(serializers.ModelSerializer):
    effect_detail = EffectSerializer(source='effect', read_only=True)

    class Meta:
        model = CardContainedEffect
        fields = ['id', 'effect', 'effect_detail', 'parameters', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CardListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listings (without expanded relationships)"""
    class Meta:
        model = Card
        fields = ['id', 'title', 'image', 'level', 'health', 'attack', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CardDetailSerializer(serializers.ModelSerializer):
    """Full serializer with all relationships"""
    races_detail = RaceSerializer(source='races', many=True, read_only=True)
    applied_buffs = CardAppliedBuffSerializer(many=True, read_only=True)
    effects = CardContainedEffectSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = [
            'id',
            'title',
            'description',
            'image',
            'level',
            'races',
            'races_detail',
            'attack',
            'health',
            'applied_buffs',
            'effects',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """Create a new card"""
        races = validated_data.pop('races', [])
        card = Card.objects.create(**validated_data)
        if races:
            card.races.set(races)
        return card

    def update(self, instance, validated_data):
        """Update an existing card"""
        races = validated_data.pop('races', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if races is not None:
            instance.races.set(races)
        return instance

from rest_framework import serializers
from .models import Buff, Efecto, Carta, CartaBuffAplicado, CartaEfectoContenido


class BuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buff
        fields = ['id', 'name', 'description', 'atributos', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class EfectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Efecto
        fields = ['id', 'name', 'description', 'atributos', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CartaBuffAplicadoSerializer(serializers.ModelSerializer):
    buff_detail = BuffSerializer(source='buff', read_only=True)

    class Meta:
        model = CartaBuffAplicado
        fields = ['id', 'buff', 'buff_detail', 'parametros', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CartaEfectoContenidoSerializer(serializers.ModelSerializer):
    efecto_detail = EfectoSerializer(source='efecto', read_only=True)

    class Meta:
        model = CartaEfectoContenido
        fields = ['id', 'efecto', 'efecto_detail', 'parametros', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CartaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados (sin relaciones expandidas)"""
    class Meta:
        model = Carta
        fields = ['id', 'titulo', 'nivel', 'vida', 'ataque', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CartaDetailSerializer(serializers.ModelSerializer):
    """Serializer completo con todas las relaciones"""
    buffs_aplicados = CartaBuffAplicadoSerializer(many=True, read_only=True)
    efectos = CartaEfectoContenidoSerializer(many=True, read_only=True)

    class Meta:
        model = Carta
        fields = [
            'id',
            'titulo',
            'descripcion',
            'imagen',
            'nivel',
            'razas',
            'ataque',
            'vida',
            'buffs_aplicados',
            'efectos',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        """Crear una nueva carta"""
        return Carta.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Actualizar una carta existente"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Buff, Efecto, Carta, CartaBuffAplicado, CartaEfectoContenido
from .serializers import (
    BuffSerializer,
    EfectoSerializer,
    CartaListSerializer,
    CartaDetailSerializer,
    CartaBuffAplicadoSerializer,
    CartaEfectoContenidoSerializer,
)


class BuffViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para Buffs.
    Los buffs se cargan desde configuración y no se editan en la aplicación.
    """
    queryset = Buff.objects.all()
    serializer_class = BuffSerializer


class EfectoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para Efectos.
    Los efectos se cargan desde configuración y no se editan en la aplicación.
    """
    queryset = Efecto.objects.all()
    serializer_class = EfectoSerializer


class CartaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para CRUD de Cartas.
    Soporta:
    - GET /cartas/ (listar)
    - GET /cartas/{id}/ (detalle con relaciones)
    - POST /cartas/ (crear)
    - PUT /cartas/{id}/ (actualizar)
    - DELETE /cartas/{id}/ (eliminar)
    - POST /cartas/{id}/add_buff/ (agregar buff a carta)
    - DELETE /cartas/{id}/remove_buff/{buff_id}/ (remover buff)
    - POST /cartas/{id}/add_efecto/ (agregar efecto a carta)
    - DELETE /cartas/{id}/remove_efecto/{efecto_id}/ (remover efecto)
    """
    queryset = Carta.objects.all().prefetch_related('buffs_aplicados', 'efectos')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CartaDetailSerializer
        return CartaListSerializer

    @action(detail=True, methods=['post'], url_path='add-buff')
    def add_buff(self, request, pk=None):
        """
        Agregar un buff aplicado a una carta.
        Body: {"buff": <buff_id>, "parametros": {...}}
        """
        carta = self.get_object()
        buff_id = request.data.get('buff')
        parametros = request.data.get('parametros', {})

        try:
            buff = Buff.objects.get(id=buff_id)
        except Buff.DoesNotExist:
            return Response(
                {'error': 'Buff no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar que los parámetros correspondan a los atributos del buff
        atributos_buff = {attr['nombre']: attr['tipo'] for attr in buff.atributos}
        for clave in parametros.keys():
            if clave not in atributos_buff:
                return Response(
                    {'error': f'Parámetro "{clave}" no está definido en los atributos del buff'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Crear o actualizar la relación
        buff_aplicado, created = CartaBuffAplicado.objects.update_or_create(
            carta=carta,
            buff=buff,
            defaults={'parametros': parametros}
        )

        serializer = CartaBuffAplicadoSerializer(buff_aplicado)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove-buff/(?P<buff_id>[^/.]+)')
    def remove_buff(self, request, pk=None, buff_id=None):
        """Remover un buff de una carta."""
        carta = self.get_object()
        try:
            CartaBuffAplicado.objects.get(carta=carta, buff_id=buff_id).delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except CartaBuffAplicado.DoesNotExist:
            return Response(
                {'error': 'Buff no aplicado a esta carta'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], url_path='add-efecto')
    def add_efecto(self, request, pk=None):
        """
        Agregar un efecto contenido a una carta.
        Body: {"efecto": <efecto_id>, "parametros": {...}}
        """
        carta = self.get_object()
        efecto_id = request.data.get('efecto')
        parametros = request.data.get('parametros', {})

        try:
            efecto = Efecto.objects.get(id=efecto_id)
        except Efecto.DoesNotExist:
            return Response(
                {'error': 'Efecto no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar que los parámetros correspondan a los atributos del efecto
        atributos_efecto = {attr['nombre']: attr['tipo'] for attr in efecto.atributos}
        for clave in parametros.keys():
            if clave not in atributos_efecto:
                return Response(
                    {'error': f'Parámetro "{clave}" no está definido en los atributos del efecto'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Crear o actualizar la relación
        efecto_contenido, created = CartaEfectoContenido.objects.update_or_create(
            carta=carta,
            efecto=efecto,
            defaults={'parametros': parametros}
        )

        serializer = CartaEfectoContenidoSerializer(efecto_contenido)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove-efecto/(?P<efecto_id>[^/.]+)')
    def remove_efecto(self, request, pk=None, efecto_id=None):
        """Remover un efecto de una carta."""
        carta = self.get_object()
        try:
            CartaEfectoContenido.objects.get(carta=carta, efecto_id=efecto_id).delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        except CartaEfectoContenido.DoesNotExist:
            return Response(
                {'error': 'Efecto no contenido en esta carta'},
                status=status.HTTP_404_NOT_FOUND
            )

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import BuffViewSet, EfectoViewSet, CartaViewSet

router = DefaultRouter()
router.register(r'buffs', BuffViewSet, basename='buff')
router.register(r'efectos', EfectoViewSet, basename='efecto')
router.register(r'cartas', CartaViewSet, basename='carta')

urlpatterns = [
    path('', include(router.urls)),
]

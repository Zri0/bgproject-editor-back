from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import BuffViewSet, EffectViewSet, RaceViewSet, CardViewSet

router = DefaultRouter()
router.register(r'buffs', BuffViewSet, basename='buff')
router.register(r'effects', EffectViewSet, basename='effect')
router.register(r'races', RaceViewSet, basename='race')
router.register(r'cards', CardViewSet, basename='card')

urlpatterns = [
    path('', include(router.urls)),
]

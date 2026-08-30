from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """Root endpoint de la API"""
    return Response({
        'message': 'Card Editor API',
        'version': '1.0.0',
        'endpoints': {
            'cartas': '/api/cartas/',
            'buffs': '/api/buffs/',
            'efectos': '/api/efectos/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/', include('cartas.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

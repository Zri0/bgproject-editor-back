from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Card Editor API',
        'version': '1.0.0',
        'endpoints': {
            'cards': '/api/cards/',
            'buffs': '/api/buffs/',
            'effects': '/api/effects/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/', include('cards.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path , include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers


schema_view = get_schema_view(
    openapi.Info(
      title="Roshan - Django Project",
      default_version='v1',
    ),
    public=True,
)

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]

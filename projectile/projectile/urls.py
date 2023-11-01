from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Change Admin Top Nav Header
admin.site.site_header = "Telehealth Admin"

urlpatterns = [
    # Swagger
    # YOUR PATTERNS
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # JWT Token
    path(
        "api/v1/token",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    # Doctor Private
    path("api/v1/doctors", include("doctorio.rest.urls")),
    # Organization Public
    path("api/v1/organizations", include("accountio.rest.urls.organizations")),
    # Core Private
    path("api/v1/me", include("core.rest.urls.me")),
    # notifications
    path("api/v1/notifications", include("core.rest.urls.notifications")),
    # Weapi Private
    path("api/v1/we", include("weapi.rest.urls")),
    # Admin
    path("adminium/", admin.site.urls),
    # django-health-check urls
    path("health/", include("health_check.urls")),
    # patientio
    path("api/v1/patient", include("patientio.rest.urls")),
    # mediaroomio
    path("api/v1/images", include("mediaroomio.rest.urls.images")),
    # threadio
    path("api/v1/calls", include("threadio.rest.urls.videocall")),
    # inbox
    path("api/v1/inbox", include("threadio.rest.urls.inbox")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .views import Home
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema.basePath = "/api/"  # API prefix
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Parikshana API",
        default_version="v1",
        description="You get all the apis , i get your data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="royimonroy@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
    authentication_classes=[BasicAuthentication, JWTAuthentication],
    generator_class=CustomOpenAPISchemaGenerator,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls", namespace="User")),
    path("ping/", Home.as_view(), name="namaste"),
    path("school/", include("school_app.urls", namespace="School")),
]


# JWT
urlpatterns += [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Final url patterns
urlpatterns = [
    path("api/", include(urlpatterns)),
]


# Silk
urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

# OPENAPI
urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

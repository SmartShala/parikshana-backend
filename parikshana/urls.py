from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
]

# Silk
urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]


# Final url patterns
urlpatterns = [path("api/", include(urlpatterns))]

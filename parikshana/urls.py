from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import Home

urlpatterns = [
    path("admin/", admin.site.urls),

]

# Silk
urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

# JWT 
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Final url patterns
urlpatterns = [
    path("api/", include(urlpatterns)),
    path('',Home.as_view()),
]



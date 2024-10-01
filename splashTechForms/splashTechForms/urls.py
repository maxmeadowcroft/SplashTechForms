from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('app/', include('authentication.urls')),
    path('app/', include('builder.urls')),
    path('', include('landing.urls'))
]

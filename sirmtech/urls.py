"""
URL configuration for sirmtech project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nysc/', include("nysc.urls", namespace="nysc")),
    path('store/', include("store.urls", namespace="store")),
]


# handler404 = 'Users.views.handler404'
# handler500 = 'Users.views.handler500'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

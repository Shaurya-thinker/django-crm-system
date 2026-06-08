from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('crm.urls')
    ),
]

handler403 = 'crm.views.custom_403'
handler404 = 'crm.views.custom_404'

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
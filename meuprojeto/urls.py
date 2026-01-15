from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    path(
        'login/',
        RedirectView.as_view(url='/accounts/login/', permanent=True)
    ),

    path('company/', include('companies.urls')),
    path('projects/', include('projects.urls')),
    path('pesquisa/', include('surveys.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

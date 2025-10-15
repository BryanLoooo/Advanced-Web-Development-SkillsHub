# import libraries and modules
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

# define url patterns
urlpatterns = [
    path("", RedirectView.as_view(url="/learnhub/login/", permanent=False)),
    path('', include('learnhub.urls')),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import include, path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("whistleblower_site.urls")),
    path("", include("allauth.urls")),
    path("", RedirectView.as_view(url='/login/'))
]

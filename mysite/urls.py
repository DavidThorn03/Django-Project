from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("holidays/", include("holidays.urls")),
    path("admin/", admin.site.urls),
]
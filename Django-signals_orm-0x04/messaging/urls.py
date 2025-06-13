from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("delete-account/", views.delete_user, name="delete_user"),
    path("admin/", admin.site.urls),
    path("", include("messaging.urls")),
]
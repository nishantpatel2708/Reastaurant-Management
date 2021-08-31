from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'kitchen'

urlpatterns = [] + static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

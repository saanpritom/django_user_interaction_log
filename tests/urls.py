from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_event_logger/', include('django_event_logger.urls'))
]

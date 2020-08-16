from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_user_interaction_log/', include('django_user_interaction_log.urls'))
]

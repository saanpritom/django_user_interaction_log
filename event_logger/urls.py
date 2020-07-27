from django.urls import path
from .views import (LogRecordsListView, LogRecordsDetailView)

urlpatterns = [
    path('', LogRecordsListView.as_view(), name='event_logger_list_view'),
    path('<int:pk>/', LogRecordsDetailView.as_view(), name='event_logger_detail_view'),
]

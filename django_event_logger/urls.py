from django.urls import path
from .views import (LogRecordsListView, LogRecordsDetailView)
from .examples import (ExampleViewWithMixin, example_function_based_view)

urlpatterns = [
    path('', LogRecordsListView.as_view(), name='event_logger_list_view'),
    path('<int:pk>/', LogRecordsDetailView.as_view(), name='event_logger_detail_view'),

    #  These are example pages urls
    path('example/mixin/', ExampleViewWithMixin.as_view(), name='event_logger_mixin_example_view'),
    path('example/function/', example_function_based_view, name='event_logger_function_example_view'),
]

from django.urls import path
from .apps import DjangoUserInteractionLogConfig
from .views import (LogRecordsListView, LogRecordsDetailView)
from .examples import (ExampleViewWithMixin, example_function_based_view)

urlpatterns = [
    path('', LogRecordsListView.as_view(), name=str(DjangoUserInteractionLogConfig.name) + '_list_view'),
    path('<int:pk>/', LogRecordsDetailView.as_view(), name=str(DjangoUserInteractionLogConfig.name) + '_detail_view'),

    #  These are example pages urls
    path('example/mixin/', ExampleViewWithMixin.as_view(), name=str(DjangoUserInteractionLogConfig.name) + '_mixin_example_view'),
    path('example/function/', example_function_based_view, name=str(DjangoUserInteractionLogConfig.name) + '_function_example_view'),
]

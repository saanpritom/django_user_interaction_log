from .registrars import create_log_record


class EventLoggerMixin:
    event_logger_log_detail_message = None
    event_logger_log_target_object = None

    def dispatch(self, request, *args, **kwargs):
        self.create_log(request=request)
        return super().dispatch(request, *args, **kwargs)

    def get_log_target_object(self, request, *args, **kwargs):
        """Return the log target object. You need to inheritet this method to send your own target_object.
           If not inheriteted then it return the default event_logger_log_target_object"""
        return self.event_logger_log_target_object

    def create_log(self, request):
        return create_log_record(request=request, log_detail=self.event_logger_log_detail_message,
                                 log_target=self.get_log_target_object(request=request))

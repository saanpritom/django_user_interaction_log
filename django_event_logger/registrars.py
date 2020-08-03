"""registrars holds the function used to create a log record. Usually these functions will be used by apps to
   create a LogRecordsModel object"""
from django.core.exceptions import ValidationError
from .models import LogRecordsModel
from .scripts import (get_request_event_path, get_request_user)


def create_log_record(request=None, log_detail=None, log_target=None):
    """This function takes arguments and process them and send them to LogRecordsModel create method to create
       a log record. However, you do not need to send any argument to this function to create a log record. If
       no arguments have passed then the record will be created using the default values.
       The first argument is request=None, Send the HttpRequest object here.
       The second argument is log_detail=None, send a nice event description text message here.
       The third argument is log_target=None, send that object on which that action was performed. As for
       example the User visited a detail page of a Book Object. In that case, you may call this function with
       these values.
       create_log_records(request, 'read operation', book.object)
       This function will return the created object if successful"""
    if log_target is not None and isinstance(log_target, (int, float, complex, str)):
        raise ValidationError('log_target must be an instance of an object or none')
    log_record_object = LogRecordsModel(log_user=get_request_user(request), log_detail=log_detail,
                                        log_target=log_target, event_path=get_request_event_path(request))
    log_record_object.save()
    return log_record_object

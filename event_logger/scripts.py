"""This file holds some functions which are used to accomplish some specific tasks"""
from django.http import HttpRequest
from django.core.exceptions import ValidationError


def get_request_event_path(request):
    """Receives a Django HttpRequest object and returns HttpRequest.path as a string if exists. If not found
       then return None instead"""
    if request is None:
        return None
    else:
        if isinstance(request, HttpRequest):
            if hasattr(request, 'path'):
                if request.path == '':
                    return None
                else:
                    return request.path
            else:
                return None
        else:
            raise ValidationError('request must be a Django HttpRequest object')

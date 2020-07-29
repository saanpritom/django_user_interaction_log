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
            if request.path == '':
                return None
            return request.path
        else:
            raise ValidationError('request must be a Django HttpRequest object')

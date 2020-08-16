"""These template tags are used to parse various object meta information for the built in templates"""
from django import template

register = template.Library()


@register.filter(name='model_object_meta_data')
def model_object_meta_data(model_object, meta_data_name):
    """Return object meta data as string if found. If not found then return None"""
    if hasattr(model_object._meta, meta_data_name):
        return getattr(model_object._meta, meta_data_name)
    else:
        return None


@register.filter(name='model_object_fields_list')
def model_object_fields_list(model_object):
    """Return all the fields of the model_object"""
    return model_object._meta.get_fields()


@register.filter(name='is_field_printable')
def is_field_printable(field_object):
    """Return True if it has verbose_name. Otherwise False and the whole field will not printed"""
    if hasattr(field_object, 'verbose_name'):
        return True
    else:
        return False


@register.filter(name='model_field_value_object')
def model_field_value_object(field_object, model_object):
    """Return the object value of this field object"""
    if hasattr(field_object, 'value_from_object'):
        return field_object.value_from_object(model_object)
    else:
        return None

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timesince import timesince as djtimesince
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.urls import reverse
from django.db import models
from .configs import ModuleConfigurations


# Create your models here.
class LogRecordsModel(models.Model):
    """LogRecordsModel holds the data for an action performed on the application. A log message consists of
        four parts. {User} + {Action} + {Target Object} + {Event Path} + {Action Time}.
        User is an instance of the User model. Every action must have a User. However, if not User is found
        then it will assign 'Anonymous' as the user.
        Action is the string representation of the log. Its just a message but it cannot be null.
        Target Object is the object on which the Action is performed. If no Target object is found then it
        will be a blank one.
        Event Path will be the URL where the action has taken place. If no URL has found then it will be null.
        Action Time represents the time and date of the action"""
    user_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name='log_user_content_type',
                                          on_delete=models.CASCADE, db_index=True, verbose_name='Log User Content Type')
    user_object_id = models.CharField(max_length=255, db_index=True, verbose_name='Log User ID', default='0')
    log_user = GenericForeignKey('user_content_type', 'user_object_id')
    log_detail = models.TextField(verbose_name='Log Detail', default='no specified operation')
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name='log_target_content_type',
                                            on_delete=models.CASCADE, db_index=True, verbose_name='Log Target Content Type')
    target_object_id = models.CharField(max_length=255, db_index=True, null=True, blank=True, verbose_name='Log Target Object ID')
    log_target = GenericForeignKey('target_content_type', 'target_object_id')
    event_path = models.TextField(verbose_name='Event Path', default='n/a')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Log Record'
        verbose_name_plural = 'Log Records'
        ordering = ['-created_at']

    def __str__(self):
        """This method returns a string representation of the full message of a log record. The message is
            constructed with the following format.
            {log_record_id} + {user} + performed + {log_message} + on + {target_object} + at + {event_path} +
            {since_time} ago"""
        if self.log_target is None:
            return str(self.id) + '. ' + self.get_user_representer() + ' performed ' + str(self.log_detail) + ' at ' + str(self.event_path) + ' ' + str(self.get_timesince()) + ' ago'
        return str(self.id) + '. ' + self.get_user_representer() + ' performed ' + str(self.log_detail) + ' on ' + str(self.log_target) + ' at ' + str(self.event_path) + ' ' + str(self.get_timesince()) + ' ago'

    def get_absolute_url(self):
        return reverse('event_logger_detail_view', args=[self.id])

    def get_user_object_absolute_url(self):
        """Return the absolute url of the User object. If not found then return #"""
        if self.log_user is not None:
            if hasattr(self.log_user, 'get_absolute_url'):
                return self.log_user.get_absolute_url()
            else:
                return '#'
        else:
            return '#'

    def get_target_object_absolute_url(self):
        """Return the absolute url of the Target object. If not found then return #"""
        if self.log_target is not None:
            if hasattr(self.log_target, 'get_absolute_url'):
                return self.log_target.get_absolute_url()
            else:
                return '#'
        else:
            return '#'

    def clean(self):
        """Customizing clean method to check if the log_user is actually an User instance. If None found then
            Anonymous user will return"""
        if self.user_object_id is None:
            self.user_object_id = str(self.__class__._meta.get_field('user_object_id').default)
        if self.log_detail is None:
            self.log_detail = str(self.__class__._meta.get_field('log_detail').default)
        if self.event_path is None:
            self.event_path = str(self.__class__._meta.get_field('event_path').default)
        if self.log_user is not None:
            if isinstance(self.log_user, get_user_model()) is False:
                raise ValidationError('The log user argument must be an User instance')
        super().clean()

    def save(self, *args, **kwargs):
        """Customizing save method to call the clean method when the save method is being called"""
        self.clean()
        super().save(*args, **kwargs)

    def is_user_anonymous(self):
        """This method True if the user_object_id is 0 otherwise False"""
        if self.user_object_id == self.__class__._meta.get_field('user_object_id').default:
            return True
        else:
            return False

    def get_user_representer(self, test_user_model_field=None):
        """This returns a string representation of the user instance. By default it calls the __str__ method
           of the user class. But if you want to change it then please add 'user_representer_field' on
           'EVENT_LOGGER_SETTINGS' at your settings file. If the user is Anonymous then it simply return Anonymous"""
        if self.log_user is None:
            return 'Anonymous'
        else:
            if test_user_model_field is None:
                user_model_field = ModuleConfigurations().get_default_user_representer_field()
            else:
                user_model_field = test_user_model_field
            if user_model_field == '__str__':
                return str(self.log_user)
            else:
                try:
                    return str(getattr(self.log_user, user_model_field))
                except AttributeError:
                    return "The selected User Representer Field doesn't exists."

    def get_timesince(self):
        """This method returns the time difference between today and the log creation time"""
        return djtimesince(self.created_at, now()).encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timesince import timesince as djtimesince
from django.utils.timezone import now
from django.conf import settings
from django.db import models


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
    user_content_type = models.ForeignKey(ContentType, null=True, blank=True,
                                          related_name='log_user', on_delete=models.CASCADE,
                                          db_index=True, verbose_name='Log User Content Type')
    user_object_id = models.CharField(max_length=255, db_index=True, verbose_name='Log User ID', default='Anonymous')
    log_user = GenericForeignKey('user_content_type', 'user_object_id')
    log_detail = models.TextField(verbose_name='Log Detail', default='no specified operation')
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name='log_target',
                                            on_delete=models.CASCADE, db_index=True,
                                            verbose_name='Log Target Content Type')
    target_object_id = models.CharField(max_length=255, null=True, blank=True, db_index=True,
                                        verbose_name='Log Target Object ID')
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
        return str(self.id) + '. ' + self.get_user_representer() + ' performed ' + self.log_detail + ' on ' + str(self.log_target) + ' at ' + self.event_path + ' ' + str(self.get_timesince()) + ' ago'

    def get_user_representer(self):
        """This returns a string representation of the user instance. By default it calls the __str__ method
           of the user class. But if you want to change it then please add 'user_representer_field' on
           'EVENT_LOGGER_SETTINGS' at your settings file. If the user is Anonymous then it simply return Anonymous"""
        if self.log_user is None:
            return str(self.__class__._meta.get_field('user_object_id').default)
        else:
            if hasattr(settings, 'EVENT_LOGGER_SETTINGS'):
                if 'user_representer_field' in settings.EVENT_LOGGER_SETTINGS:
                    return str(getattr(self.log_user, settings.EVENT_LOGGER_SETTINGS['user_representer_field']))
                else:
                    return str(self.log_user)
            else:
                return str(self.log_user)

    def get_timesince(self):
        """This method returns the time difference between today and the log creation time"""
        return djtimesince(self.created_at, now()).encode('utf8').replace(b'\xc2\xa0', b' ').decode('utf8')

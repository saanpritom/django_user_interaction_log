from django.db import models


# Create your models here.
class LogRecordsModel(models.Model):
    """LogRecordsModel holds the details about the events occured accross the application. Currenty this model
       has 6 fields. An unique ID which is auto incremented, The actor who perform any events on the application
       usually an instance of the User model, A text field contains details about the log, The targeted model
       instance ID on which that task has performed, The path of that view where that tasks occured and the
       event date and time"""
    actor_id = models.CharField(max_length=80, null=True, blank=True, verbose_name='Actor ID', default='0')
    log_detail = models.TextField(null=True, blank=True, verbose_name='Log Detail', default='n/a')
    targeted_instance_id = models.CharField(max_length=80, null=True, blank=True, verbose_name='Targeted Instance ID',
                                            default='0')
    event_path = models.TextField(null=True, blank=True, verbose_name='Event Path', default='n/a')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Log Record'
        verbose_name_plural = 'Log Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.actor_id

    def get_anonymous_object(self, current_value, default_value):
        """This classmethod takes two arguments current_value and default_value and check if those matched.
           If matched then return 'Anonymous' as object text"""
        if current_value == default_value:
            return 'Anonymous'
        else:
            return current_value

    def get_full_message(self):
        """This classmethod constacts a full action message for quicker usage. It first checks if the _id marked
           fields values are in default stage. If default value found then the value is changed to Anonymous
           to the message. Returns a string representation of a LogRecordsModel instance.
           The structure of the string is:
           {actor_id} + ' performed ' + {log_detail} + ' on ' + {targeted_instance_id} + ' at ' + {event_path} +
           ' at ' + {created_at}"""
        message = ''
        message = str(self.get_anonymous_object(self.actor_id, self.__class__._meta.get_field('actor_id').default))
        message = message + ' performed ' + str(self.log_detail) + ' on '
        message = message + str(self.get_anonymous_object(self.targeted_instance_id, self.__class__._meta.get_field('targeted_instance_id').default))
        message = message + ' at ' + str(self.event_path) + ' at ' + str(self.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        return message

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

    def __str__(self):
        return self.actor_id

    class Meta:
        verbose_name = 'Log Record'
        verbose_name_plural = 'Log Records'
        ordering = ['-created_at']

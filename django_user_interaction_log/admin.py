from django.contrib import admin
from .models import LogRecordsModel


# Register your models here.
class DjangoUserInteractionLogAdmin(admin.ModelAdmin):
    list_display = ['user_object_id', 'log_detail', 'target_object_id',
                    'event_path', 'log_time']
    search_fields = ['user_object_id', 'target_object_id']

    def log_time(self, obj):
        return str(obj.get_timesince()) + ' ago'


admin.site.register(LogRecordsModel, DjangoUserInteractionLogAdmin)

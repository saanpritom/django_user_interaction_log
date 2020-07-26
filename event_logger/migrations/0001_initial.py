# Generated by Django 3.0 on 2020-07-26 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogRecordsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_object_id', models.CharField(db_index=True, default='Anonymous', max_length=255, verbose_name='Log User ID')),
                ('log_detail', models.TextField(verbose_name='Log Detail')),
                ('target_object_id', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Log Target Object ID')),
                ('event_path', models.TextField(blank=True, default='n/a', null=True, verbose_name='Event Path')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('target_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_target', to='contenttypes.ContentType', verbose_name='Log Target Content Type')),
                ('user_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_user', to='contenttypes.ContentType', verbose_name='Log User Content Type')),
            ],
            options={
                'verbose_name': 'Log Record',
                'verbose_name_plural': 'Log Records',
                'ordering': ['-created_at'],
            },
        ),
    ]

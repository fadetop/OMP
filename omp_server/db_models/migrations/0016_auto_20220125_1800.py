# Generated by Django 3.1.4 on 2022-01-25 18:00

from django.db import migrations, models

from db_models.models import MainInstallHistory, UpgradeHistory, \
    RollbackHistory, ExecutionRecord
from db_models.receivers.execution_record import create_execution_record


def update_execution_record(apps, schema_editor):
    ExecutionRecord.objects.all().delete()
    for model in [MainInstallHistory, UpgradeHistory, RollbackHistory]:
        histories = model.objects.all()
        for history in histories:
            create_execution_record(history)


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0015_executionrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executionrecord',
            name='module_id',
            field=models.CharField(default='0', max_length=36, verbose_name='执行记录的id'),
        ),
        migrations.RunPython(update_execution_record),
    ]

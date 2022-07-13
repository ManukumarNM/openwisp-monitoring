# Generated by Django 3.0.3 on 2020-08-05 12:20

from django.db import migrations

from openwisp_monitoring.monitoring.configuration import get_metric_configuration


def make_fields_null(apps, schema_editor):
    """
    This function checks the values of alertsettings fields,
    if the values match default values provided in the metric configuration
    then those values will be set as None.

    It will also convert tolerance field values from seconds to minutes
    and update old notification types.
    """
    AlertSettings = apps.get_model('monitoring', 'AlertSettings')
    Notification = apps.get_model('openwisp_notifications', 'Notification')
    for alert_settings in AlertSettings.objects.all():
        config_name = alert_settings.metric.configuration
        metric_config = get_metric_configuration()[config_name]
        alertsettings_config = metric_config['alert_settings']
        notifications_queryset = Notification.objects.filter(
            action_object_object_id=alert_settings.pk
        )
        if notifications_queryset:
            migrate_notifications(
                queryset=notifications_queryset,
                notification_config=metric_config['notification'],
                metric_config_name=config_name,
            )
        if alert_settings.custom_threshold == alertsettings_config['threshold']:
            alert_settings.custom_threshold = None
        if alert_settings.custom_tolerance // 60 == alertsettings_config['tolerance']:
            alert_settings.custom_tolerance = None
        else:
            alert_settings.custom_tolerance //= 60
        if alert_settings.custom_operator == alertsettings_config['operator']:
            alert_settings.custom_operator = None
        alert_settings.save()


def migrate_notifications(queryset, notification_config, metric_config_name):
    for notification in queryset:
        if notification.type == 'threshold_crossed':
            notification.type = f'{metric_config_name}_problem'
            notification.verb = notification_config['problem']['verb']
        elif notification.type == 'threshold_recovery':
            notification.type = f'{metric_config_name}_recovery'
            notification.verb = notification_config['recovery']['verb']
        notification.save()


def reverse_null_fields(apps, schema_editor):
    """
    This function checks the values of alertsettings fields,
    if the values are None then they are replaced by default
    values provided in the metric configuration.

    It will also revert conversion of tolerance field values from seconds to minutes
    and notification types.
    """
    AlertSettings = apps.get_model('monitoring', 'AlertSettings')
    Notification = apps.get_model('openwisp_notifications', 'Notification')
    for alert_settings in AlertSettings.objects.all():
        config_name = alert_settings.metric.configuration
        metric_config = get_metric_configuration()[config_name]
        alertsettings_config = metric_config['alert_settings']
        notifications_queryset = Notification.objects.filter(
            action_object_object_id=alert_settings.pk
        )
        if notifications_queryset:
            reverse_migrate_notifications(notifications_queryset, config_name)
        if alert_settings.custom_threshold is None:
            alert_settings.custom_threshold = alertsettings_config['threshold']
        if alert_settings.custom_tolerance is None:
            alert_settings.custom_tolerance = alertsettings_config['tolerance'] * 60
        else:
            alert_settings.custom_tolerance *= 60
        if alert_settings.custom_operator is None:
            alert_settings.custom_operator = alertsettings_config['operator']
        alert_settings.save()


def reverse_migrate_notifications(queryset, metric_config_name):
    for notification in queryset:
        if notification.type == f'{metric_config_name}_problem':
            notification.type = 'threshold_crossed'
            notification.verb = 'crossed the threshold'
        elif notification.type == f'{metric_config_name}_recovery':
            notification.type = 'threshold_recovery'
            notification.verb = 'returned within the threshold'
        notification.save()


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0019_rename_alertsettings_fields'),
        ('openwisp_notifications', '0003_notification_notification_type'),
    ]

    operations = [
        migrations.RunPython(make_fields_null, reverse_code=reverse_null_fields)
    ]

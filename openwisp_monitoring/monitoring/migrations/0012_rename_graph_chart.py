# Generated by Django 3.0.3 on 2020-06-01 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [('monitoring', '0011_alert_settings_contenttype_registration')]

    operations = [
        migrations.AlterModelTable(name='graph', table='monitoring_chart'),
        migrations.RenameModel(old_name='Graph', new_name='Chart'),
        migrations.AlterModelTable(name='chart', table=None),
        migrations.AlterModelOptions(
            name='alertsettings',
            options={
                'verbose_name': 'Alert settings',
                'verbose_name_plural': 'Alert settings',
            },
        ),
    ]

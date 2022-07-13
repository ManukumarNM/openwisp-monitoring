# Generated by Django 3.0.4 on 2020-04-28 17:22

from django.db import migrations, models

from ..configuration import CHART_CONFIGURATION_CHOICES


class Migration(migrations.Migration):

    dependencies = [('monitoring', '0005_metric_is_heathy_unknown')]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='configuration',
            field=models.CharField(
                choices=CHART_CONFIGURATION_CHOICES, max_length=16, null=True
            ),
        )
    ]
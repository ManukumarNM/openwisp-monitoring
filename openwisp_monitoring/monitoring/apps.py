from time import sleep

from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from requests.exceptions import ConnectionError
from swapper import get_model_name

from openwisp_utils.admin_theme.menu import register_menu_group

from ..db import timeseries_db
from .configuration import get_metric_configuration, register_metric_notifications


class MonitoringConfig(AppConfig):
    name = 'openwisp_monitoring.monitoring'
    label = 'monitoring'
    verbose_name = _('Network Monitoring')
    max_retries = 5
    retry_delay = 3

    def ready(self):
        self.create_database()
        setattr(settings, 'OPENWISP_ADMIN_SHOW_USERLINKS_BLOCK', True)
        metrics = get_metric_configuration()
        for metric_name, metric_config in metrics.items():
            register_metric_notifications(metric_name, metric_config)
        self.register_menu_groups()

    def create_database(self):
        # create Timeseries database if it doesn't exist yet
        for attempt_number in range(1, self.max_retries + 1):
            try:
                timeseries_db.create_database()
                return
            except ConnectionError as e:
                self.warn_and_delay(attempt_number)
                if attempt_number == self.max_retries:
                    raise e

    def warn_and_delay(self, attempt_number):
        print(
            'Got error while connecting to timeseries database. '
            f'Retrying again in 3 seconds (attempt n. {attempt_number} out of 5).'
        )
        sleep(self.retry_delay)

    def register_menu_groups(self):
        register_menu_group(
            position=80,
            config={
                'label': 'Monitoring',
                'items': {
                    1: {
                        'label': _('Metrics'),
                        'model': get_model_name('monitoring', 'Metric'),
                        'name': 'changelist',
                        'icon': 'ow-metrics',
                    },
                    2: {
                        'label': _('Checks'),
                        'model': get_model_name('check', 'Check'),
                        'name': 'changelist',
                        'icon': 'ow-monitoring-checks',
                    },
                },
                'icon': 'ow-monitoring',
            },
        )

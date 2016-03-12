from django.core.management.base import BaseCommand
from django_iot.apps.interactions.tasks import set_status


class Command(BaseCommand):
    help = 'Set device status for one device id'

    def add_arguments(self, parser):
        parser.add_argument('device_id', type=int)
        parser.add_argument('status_message', type=str)

    def handle(self, *args, **options):
        status_pk = set_status(options['device_id'], options['status_message'])
        self.stdout.write('Set status %s to %s for device %d' % (status_pk, options['status_message'], options['device_id']))

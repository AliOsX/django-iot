from django.core.management.base import BaseCommand
from django_iot.apps.interactions.tasks import pull_status


class Command(BaseCommand):
    help = 'Get device status for listed device ids'

    def add_arguments(self, parser):
        parser.add_argument('device_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for pk in options['device_id']:
            status_pks = pull_status(pk)
            self.stdout.write('Got status %s for device %d' % (status_pks, pk))

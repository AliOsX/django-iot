from django.core.management.base import BaseCommand
from django_iot.apps.interactions.tasks import pull_data


class Command(BaseCommand):
    help = 'Get device observations for listed device ids'

    def add_arguments(self, parser):
        parser.add_argument('device_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for pk in options['device_id']:
            obs_pks = pull_data(pk)
            self.stdout.write('Got observations %s for device %d' % (obs_pks, pk))

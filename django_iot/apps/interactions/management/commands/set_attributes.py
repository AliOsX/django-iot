from django.core.management.base import BaseCommand
from django_iot.apps.interactions.tasks import set_attributes


class Command(BaseCommand):
    help = 'Set device status for one device id'

    def add_arguments(self, parser):
        parser.add_argument('device_id', type=int)
        parser.add_argument('color', type=str)
        parser.add_argument('brightness', type=float)

    def handle(self, *args, **options):
        attr_pks = set_attributes(options['device_id'],
                                  color=options['color'],
                                  brightness=options['brightness'])
        self.stdout.write('Set attributes %s  for device %d' % (attr_pks, options['device_id']))

from django.core.management.base import BaseCommand
from django_iot.apps.interactions import tasks


class Command(BaseCommand):
    help = 'Run an interaction task'

    def add_arguments(self, parser):
        parser.add_argument('task_name')
        parser.add_argument('--device_id', required=False, type=int)
        parser.add_argument('--is_on', required=False, type=bool)
        parser.add_argument('--color', required=False, type=str)
        parser.add_argument('--brightness', required=False, type=float)
        parser.add_argument('--hashtag', required=False, type=str)
        parser.add_argument('--votechoices', required=False, type=str,
                            help='comma-separated list, eg red,blue,yellow')

    def handle(self, *args, **options):
        # get task
        task_fn = getattr(tasks, options['task_name'])

        # parse args
        try:
            options['votechoices'] = options['votechoices'].split(',')
        except AttributeError:  # None if not provided
            options.pop('votechoices')

        # run task with args
        result = task_fn(**options)
        self.stdout.write('Ran %s with result %s' % (options['task_name'], result))

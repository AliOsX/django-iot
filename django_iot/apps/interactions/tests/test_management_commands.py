from django.test import TestCase
from django.core.management import call_command
from django_iot.apps.devices.models import Device
from StringIO import StringIO
from mock import patch


class TestPullStatus(TestCase):
    def setUp(self):
        self.device1 = Device.objects.create(manufacturer_id=1)
        self.device2 = Device.objects.create(manufacturer_id=2)

        self.stdout = StringIO()

    @patch('django_iot.apps.interactions.tasks.client.get_status')
    def test_pull_one(self, mock_method):
        mock_method.return_value = 'on'

        # call command for one
        call_command('pull_status',
                     str(self.device1.pk),
                     stdout=self.stdout)

        # one has status set
        self.assertEqual(self.device1.powerstatus_set.count(), 1)
        self.assertEqual(self.device2.powerstatus_set.count(), 0)

    @patch('django_iot.apps.interactions.tasks.client.get_status')
    def test_pull_two(self, mock_method):
        mock_method.return_value = 'on'

        # call command for both
        call_command('pull_status',
                     str(self.device1.pk), str(self.device2.pk),
                     stdout=self.stdout)

        # one has status set
        self.assertEqual(self.device1.powerstatus_set.count(), 1)
        self.assertEqual(self.device2.powerstatus_set.count(), 1)


class TestPullData(TestCase):
    def setUp(self):
        self.device1 = Device.objects.create(manufacturer_id=1)
        self.device2 = Device.objects.create(manufacturer_id=2)

        self.stdout = StringIO()

    @patch('django_iot.apps.interactions.tasks.client.get_observations')
    def test_pull_one(self, mock_method):
        mock_method.return_value = {'dummy': 15, 'hexcolor': '#000'}
        # call command for one
        call_command('pull_data',
                     str(self.device1.pk),
                     stdout=self.stdout)

        # one has status set
        self.assertEqual(self.device1.attribute_set.count(), 1)
        self.assertEqual(self.device2.attribute_set.count(), 0)

    @patch('django_iot.apps.interactions.tasks.client.get_observations')
    def test_pull_two(self, mock_method):
        # use function because key gets popped on first call
        mock_method.side_effect = lambda x: {'dummy': 15, 'hexcolor': '#000'}

        # call command for both
        call_command('pull_data',
                     str(self.device1.pk), str(self.device2.pk),
                     stdout=self.stdout)

        # one has status set
        self.assertEqual(self.device1.attribute_set.count(), 1)
        self.assertEqual(self.device2.attribute_set.count(), 1)


class TestSetStatus(TestCase):
    def setUp(self):
        self.device1 = Device.objects.create(manufacturer_id=1)
        self.device2 = Device.objects.create(manufacturer_id=2)

        self.stdout = StringIO()

    @patch('django_iot.apps.interactions.tasks.client.set_status')
    def test_set_one(self, mock_method):
        mock_method.return_value = {
            'id': self.device1.pk,
            'status': 'ok',
        }

        # call command for one
        call_command('set_status',
                     str(self.device1.pk), 'dummy',
                     stdout=self.stdout)

        # one has status set
        self.assertEqual(self.device1.powerstatus_set.count(), 1)
        self.assertEqual(self.device2.powerstatus_set.count(), 0)

        # status has message
        self.assertEqual(self.device1.powerstatus_set.first().is_on, True)


class TestSetAttributes(TestCase):
    def setUp(self):
        self.device1 = Device.objects.create(manufacturer_id=1)
        self.device2 = Device.objects.create(manufacturer_id=2)

        self.stdout = StringIO()

    @patch('django_iot.apps.interactions.tasks.client.set_color')
    @patch('django_iot.apps.interactions.tasks.client.get_observations')
    def test_set_one(self, mock_get, mock_set):
        mock_set.return_value = {
            'id': self.device1.pk,
            'status': 'ok',
        }
        mock_get.return_value = {'dummy': 10, 'hexcolor': '#000'}

        # call command for one
        call_command('set_attributes',
                     str(self.device1.pk), 'dummy', '0.5',
                     stdout=self.stdout)

        # one has status set
        self.assertEqual(self.device1.attribute_set.count(), 1)
        self.assertEqual(self.device2.attribute_set.count(), 0)

        # status has message
        self.assertEqual(self.device1.attribute_set.first().units, 'dummy')

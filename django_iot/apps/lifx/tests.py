from django.test import TestCase
from django.conf import settings
from unittest import skipIf
from django_iot.apps.lifx import client
from django_iot.apps.devices.models import Device


class TestConfigure(TestCase):
    def test_configure_once(self):
        # no devices before
        self.assertEqual(Device.objects.count(), 0)

        # configure
        results = client.configure_devices()
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], Device.objects.first().pk)
        self.assertTrue(results[0][1])

    def test_configure_twice(self):
        # configure twice
        client.configure_devices()
        results = client.configure_devices()

        # test only one created
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], Device.objects.first().pk)
        self.assertFalse(results[0][1])


class TestGetAttributes(TestCase):
    def setUp(self):
        client.configure_devices()
        self.device = Device.objects.first()

    def test_get(self):
        result = client.get_attributes(self.device.pk)
        self.assertItemsEqual(result.keys(),
                              ['brightness', 'hue', 'saturation', 'kelvin'])


class TestGetStatus(TestCase):
    def setUp(self):
        client.configure_devices()
        self.device = Device.objects.first()

    def test_get(self):
        result = client.get_status(self.device.pk)
        self.assertIn(result, ['on', 'off'])


@skipIf(settings.SKIP_INTEGRATION_TESTS, 'integration tests')
class TestSetStatus(TestCase):
    def setUp(self):
        client.configure_devices()
        self.device = Device.objects.first()

    def test_turn_on(self):
        result = client.turn_on(self.device.pk)
        self.assertEqual(result['id'], self.device.manufacturer_id)
        self.assertEqual(result['label'], self.device.name)
        self.assertEqual(result['status'], 'ok')

    def test_turn_off(self):
        result = client.turn_off(self.device.pk)
        self.assertEqual(result['id'], self.device.manufacturer_id)
        self.assertEqual(result['label'], self.device.name)
        self.assertEqual(result['status'], 'ok')

    def test_green(self):
        result = client.set_color(self.device.pk, color='green')
        self.assertEqual(result['id'], self.device.manufacturer_id)
        self.assertEqual(result['label'], self.device.name)
        self.assertEqual(result['status'], 'ok')

    def test_dim(self):
        result = client.set_color(self.device.pk, brightness=0.5)
        self.assertEqual(result['id'], self.device.manufacturer_id)
        self.assertEqual(result['label'], self.device.name)
        self.assertEqual(result['status'], 'ok')


@skipIf(settings.SKIP_INTEGRATION_TESTS, 'integration tests')
class TestEffects(TestCase):
    def setUp(self):
        client.configure_devices()
        self.device = Device.objects.first()

    def test_breathe(self):
        result = client.breathe(
            self.device.pk,
            to_color='blue', from_color='yellow',
            n_cycles=3, period_seconds=3,
        )
        self.assertEqual(result['id'], self.device.manufacturer_id)
        self.assertEqual(result['label'], self.device.name)
        self.assertEqual(result['status'], 'ok')

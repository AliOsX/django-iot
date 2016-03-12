from rest_framework.test import APITestCase
from django_iot.apps.devices.models import Device
from mock import patch


class TestPullStatus(APITestCase):
    def setUp(self):
        device = Device.objects.create()
        self.url = '/api/interactions/pull_status/'
        self.data = {'device_id': device.pk}

    def test_get_fails(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')

    @patch('django_iot.apps.interactions.tasks.client.get_status')
    def test_post_response(self, mock_method):
        mock_method.return_value = 'on'
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertItemsEqual(response.data.keys(),
                              ['id', 'device', 'is_on', 'created_at', 'valid_at'])
        self.assertEqual(response.data['device'], self.data['device_id'])

    def test_post_bad_device_fails(self):
        self.data['device_id'] += 1
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['device_id'],
                         ['No device available with id %d' % self.data['device_id']])


class TestSetStatus(APITestCase):
    def setUp(self):
        device = Device.objects.create()
        self.url = '/api/interactions/set_status/'
        self.data = {'device_id': device.pk, 'is_on': True}

    def test_get_fails(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')

    @patch('django_iot.apps.interactions.tasks.client.set_status')
    def test_post_response(self, mock_method):
        mock_method.return_value = {
            'id': self.data['device_id'],
            'status': 'ok',
        }
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertItemsEqual(response.data.keys(),
                              ['id', 'device', 'is_on', 'created_at', 'valid_at'])
        self.assertEqual(response.data['device'], self.data['device_id'])
        self.assertEqual(response.data['is_on'], self.data['is_on'])

    def test_post_bad_device_fails(self):
        self.data['device_id'] += 1
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['device_id'],
                         ['No device available with id %d' % self.data['device_id']])


class TestPullData(APITestCase):
    def setUp(self):
        device = Device.objects.create()
        self.url = '/api/interactions/pull_data/'
        self.data = {'device_id': device.pk}

    def test_get_fails(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')

    @patch('django_iot.apps.interactions.tasks.client.get_observations')
    def test_post_response(self, mock_method):
        mock_method.return_value = {'dummy': 15, 'hexcolor': '#000'}
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertItemsEqual(response.data.keys(),
                              ['id', 'device', 'value', 'units', 'created_at', 'valid_at'])
        self.assertEqual(response.data['device'], self.data['device_id'])
        self.assertEqual(response.data['value'], 15)
        self.assertEqual(response.data['units'], 'dummy')

    def test_post_bad_device_fails(self):
        self.data['device_id'] += 1
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['device_id'],
                         ['No device available with id %d' % self.data['device_id']])


class TestSetAttributes(APITestCase):
    def setUp(self):
        device = Device.objects.create()
        self.url = '/api/interactions/set_attributes/'
        self.data = {'device_id': device.pk, 'color': 'blue', 'brightness': 0.5}

    def test_get_fails(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')

    @patch('django_iot.apps.interactions.tasks.client.set_color')
    @patch('django_iot.apps.interactions.tasks.client.get_observations')
    def test_post_response(self, mock_obs, mock_color):
        mock_color.return_value = {
            'id': self.data['device_id'],
            'status': 'ok',
        }
        mock_obs.return_value = {'dummy': 15, 'hexcolor': '#000'}
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertItemsEqual(response.data.keys(),
                              ['id', 'device', 'value', 'units', 'created_at', 'valid_at'])
        self.assertEqual(response.data['device'], self.data['device_id'])
        self.assertEqual(response.data['value'], 15)
        self.assertEqual(response.data['units'], 'dummy')

    def test_post_bad_device_fails(self):
        self.data['device_id'] += 1
        response = self.client.post(self.url, self.data, format='json', follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['device_id'],
                         ['No device available with id %d' % self.data['device_id']])

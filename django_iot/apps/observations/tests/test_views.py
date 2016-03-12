from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from django_iot.apps.devices.models import Device
from django_iot.apps.observations.models import Attribute
from datetime import timedelta


class TestAttributeListView(APITestCase):
    def setUp(self):
        # set up devices
        self.device1 = Device.objects.create(name='my toi 1',
                                             device_type='TOI',
                                             location='robohome',
                                             manufacturer_id='1')
        self.device2 = Device.objects.create(name='my toi 2',
                                             device_type='TOI',
                                             location='robohome',
                                             manufacturer_id='2')

        # set up observations going backward in time
        sample_time = timezone.now()
        for ihour in range(10):
            Attribute.objects.create(
                valid_at=sample_time-timedelta(hours=ihour),
                value=ihour*0.5,
                units='kW',
                device=self.device1,
            )

        for ihour in range(7):
            Attribute.objects.create(
                valid_at=sample_time-timedelta(hours=ihour),
                value=ihour*0.7,
                units='kW',
                device=self.device2,
            )

        # url
        self.url = reverse('attribute-list')

    def test_get_empty(self):
        # delete observations
        Attribute.objects.all().delete()

        # response is empty list
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 0)

    def test_paginated(self):
        response = self.client.get(self.url)
        self.assertItemsEqual(response.data.keys(),
                              ['count', 'next', 'previous', 'results'])

    def test_get_all_data(self):
        # response is full list
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 10+7)

    def test_filter_device_pk(self):
        response = self.client.get(self.url, data={'device': self.device1.pk})
        self.assertEqual(len(response.data['results']), 10)

    def test_get_data_is_ordered(self):
        # response is ordered
        response = self.client.get(self.url)
        sorted_data = sorted(response.data['results'], key=lambda x: x['valid_at'])
        self.assertEqual(response.data['results'], sorted_data)


class TestAttributeDetailView(APITestCase):
    def setUp(self):
        # set up device
        self.device = Device.objects.create(name='my toi',
                                            device_type='TOI',
                                            location='robohome')

        # set up obs
        self.obs = Attribute.objects.create(
            valid_at=timezone.now(),
            value=10,
            units='kW',
            device=self.device,
        )

        # url
        self.url = reverse('attribute-detail', kwargs={'pk': self.obs.pk})

    def test_get_data(self):
        response = self.client.get(self.url)
        expected_keys = ['id', 'created_at', 'valid_at', 'value', 'units', 'device']
        self.assertItemsEqual(response.data.keys(), expected_keys)

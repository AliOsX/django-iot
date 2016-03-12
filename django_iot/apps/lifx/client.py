from django_iot.apps.devices.models import Device
from os import environ
import requests
from colour import Color


HEADERS = {
    'Authorization': 'Bearer %s' % environ.get('LIFX_TOKEN'),
}

BASE_URL = 'https://api.lifx.com/v1/lights/'


def configure_devices():
    """
    Create all available devices,
    and update existing ones with cuurent metadata
    """
    # make request
    url = BASE_URL + 'all'
    response = requests.get(url, headers=HEADERS)

    # process
    results = []
    for data in response.json():
        # get or create
        device, created = Device.objects.get_or_create(manufacturer_id=data['id'])

        # update
        device.name = data['label']
        device.location = data['location']['name']
        device.device_type = 'LIFX'
        device.save()

        # log
        results.append((device.pk, created))

    # return
    return results


def make_request(url, method='get', data=None):
    # make and parse request
    response = getattr(requests, method)(url, data=data, headers=HEADERS)
    json_data = response.json()

    # error
    if 'error' in json_data.keys():
        raise RuntimeError(json_data['error'])

    # return
    return json_data


def get_observations(device_pk):
    """Get dict of numerical observations"""
    # make request
    selector = 'id:%s' % Device.objects.get(pk=device_pk).manufacturer_id
    url = BASE_URL + selector
    data = make_request(url)[0]

    # assemble result
    result = {
        'brightness': data['brightness'],
        'hue': data['color']['hue'],
        'saturation': data['color']['saturation'],
        'kelvin': data['color']['kelvin'],
    }

    # add hex
    color = Color(hue=result['hue'],
                  saturation=result['saturation'],
                  luminance=result['brightness'])
    result['hexcolor'] = color.hex

    # return
    return result


def get_status(device_pk):
    """Returns 'on' or 'off' """
    # make request
    selector = 'id:%s' % Device.objects.get(pk=device_pk).manufacturer_id
    url = BASE_URL + selector
    data = make_request(url)[0]

    # return
    return data['power']


def set_status(device_pk, payload):
    # make request
    selector = 'id:%s' % Device.objects.get(pk=device_pk).manufacturer_id
    url = BASE_URL + selector + '/state'
    data = make_request(url, method='put', data=payload)

    # return
    try:
        return data['results'][0]
    except KeyError:
        return data


def breathe(device_pk,
            to_color, from_color=None,
            n_cycles=5, period_seconds=1):
    # set up payload
    payload = {
        'color': to_color,
        'cycles': n_cycles,
        'period': period_seconds,
    }
    if from_color:
        payload['from_color'] = from_color

    # make request
    selector = 'id:%s' % Device.objects.get(pk=device_pk).manufacturer_id
    url = BASE_URL + selector + '/effects/breathe'
    data = make_request(url, method='post', data=payload)

    # return
    return data['results'][0]


def turn_on(device_pk):
    payload = {'power': 'on'}
    return set_status(device_pk, payload)


def turn_off(device_pk):
    payload = {'power': 'off'}
    return set_status(device_pk, payload)


def set_color(device_pk, color=None, brightness=None):
    payload = {}
    if color:
        payload['color'] = color
    if brightness:
        payload['brightness'] = brightness
    return set_status(device_pk, payload)

from django.utils import timezone
from django_iot.apps.devices.models import Device
from django_iot.apps.lifx import client
from django_iot.apps.interactions.models import TwitterVote
from celery import shared_task


@shared_task
def pull_attributes(device_id=None, **kwargs):
    """
    Pulls attribute data from the device vendor's API,
    stores the attributes in the database,
    and returns the pks of the attributes.
    """
    # check device exists
    device = Device.objects.get(pk=device_id)

    # fetch attributes
    data = client.get_attributes(device_id)

    # create color
    hexcolor = data.pop('hexcolor')
    device.color_set.create(
        hex_string=hexcolor,
        valid_at=timezone.now(),
    )

    # create observations
    pks = []
    for units, value in data.iteritems():
        obs = device.attribute_set.create(
            valid_at=timezone.now(),
            value=value,
            units=units,
        )
        pks.append(obs.pk)

    # return pk
    return pks


@shared_task
def pull_status(device_id=None, **kwargs):
    """
    Pulls the current device status from the device vendor's API,
    stores the status in the database,
    and returns the pks of the status.
    """
    # check device exists
    device = Device.objects.get(pk=device_id)

    # fetch status
    status_message = client.get_status(device_id)

    # create status
    if status_message == 'on':
        is_on = True
    else:
        is_on = False
    status = device.powerstatus_set.create(
        valid_at=timezone.now(),
        is_on=is_on,
    )

    # return pk
    return [status.pk]


@shared_task
def refresh_all(**kwargs):
    """
    Refreshes data and status for all devices
    """
    for device in Device.objects.all():
        pull_status(device.pk)
        pull_attributes(device.pk)


@shared_task
def set_status(device_id=None, is_on=True, **kwargs):
    """
    Sets the device status using the device vendor's API,
    stores the new status in the database,
    and returns the pks of the status.
    """
    # check device exists
    device = Device.objects.get(pk=device_id)

    # turn on or off
    if is_on:
        result = client.turn_on(device_id)
    else:
        result = client.turn_off(device_id)

    # create status
    if result['status'] == 'ok':
        status = device.powerstatus_set.create(
            valid_at=timezone.now(),
            is_on=is_on,
        )

        # return pk
        return [status.pk]
    else:
        return []


@shared_task
def set_attributes(device_id=None, **kwargs):
    """
    Sets the device attributes using the device vendor's API,
    stores the new attributes in the database,
    and returns the pks of the attributes.
    """
    # set attributes
    client.set_color(device_id, **kwargs)

    # log by pulling fresh data
    return pull_attributes(device_id)


@shared_task
def run_twitter_vote(device_id=None, hashtag='#DjangoIoT',
                     **kwargs):
    # run voting
    voter = TwitterVote.objects.create(hashtag=hashtag)
    top_choice, brightness = voter.collect_votes()

    # set color based on top vote
    return set_attributes(device_id, color=top_choice, brightness=brightness)

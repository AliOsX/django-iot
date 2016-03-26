from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django_iot.apps.devices.models import Device
from django_iot.apps.interactions.models import TwitterVote


def home(request):
    # set up context
    context = {'devices': [], 'vote': None}

    # collect info for devices
    for device in Device.objects.all():
        # basic data
        device_data = {
            'name': device.name,
            'location': device.location,
        }

        # current status
        try:
            current_status = device.powerstatus_set.latest('valid_at')
            if current_status.is_on:
                device_data['status_message'] = 'on'
            else:
                device_data['status_message'] = 'off'
            device_data['status_time'] = current_status.valid_at
        except ObjectDoesNotExist:
            device_data['status_message'] = '[unknown]'
            device_data['status_time'] = None

        # current color
        try:
            current_color = device.color_set.latest('valid_at')
            device_data['hex_string'] = current_color.hex_string
            device_data['color_time'] = current_color.valid_at
        except ObjectDoesNotExist:
            device_data['hexcolor'] = '[unknown]'
            device_data['color_time'] = None

        # current brightness
        try:
            current_brightness = device.attribute_set.filter(units='brightness').latest('valid_at')
            device_data['brightness'] = int(current_brightness.value * 100)
            device_data['brightness_time'] = current_color.valid_at
        except ObjectDoesNotExist:
            device_data['brightness'] = '[unknown]'
            device_data['brightness_time'] = None

        # add to storage
        context['devices'].append(device_data)

    # latest vote
    context['vote'] = {
        'choices': TwitterVote.VOTE_CHOICE_LIST,
    }
    try:
        current_vote = TwitterVote.objects.latest('created_at')
        tally_count_list = [int(v) for v in current_vote.tally.split(',')]
        unsorted_tallies = zip(current_vote.VOTE_CHOICE_LIST, tally_count_list)
        context['vote'].update({
            'tallies': reversed(sorted(unsorted_tallies, key=lambda x: x[1])),
            'hashtag': current_vote.hashtag,
            'log': current_vote.log.split(current_vote.LOG_LINE_SEP),
        })
    except ObjectDoesNotExist:
        pass

    # return
    return render(request, 'index.html', context)

NAME_TO_HEX = {
    'red': '#ff0000',
    'orange': '#ff9900',
    'yellow': '#ffff00',
    'green': '#00ff00',
    'cyan': '#00ffff',
    'blue': '#0000ff',
    'purple': '#9900ff',
    'pink': '#ff00ff',
}

HUE_RANGE = {
    'red': (0, 20),  # expected 0
    'orange': (20, 50),  # expected 36
    'yellow': (50, 100),  # expected 60
    'green': (100, 150),  # expected 120
    'cyan': (150, 220),  # expected 180
    'blue': (220, 270),  # expected 250
    'purple': (270, 300),  # expected 280
    'pink': (300, 400),  # expected 325
}


def hue_to_color_name(hue):
    # check each hue range
    for name, (hue_min, hue_max) in HUE_RANGE.iteritems():
        if hue >= hue_min and hue < hue_max:
            return name

    # if got here, no match
    raise ValueError('No color name found for hue %s' % hue)

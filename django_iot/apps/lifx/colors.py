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


def hue_to_hex(hue):
    tol = 5
    if hue < 36 - tol:
        return NAME_TO_HEX['red']
    elif hue < 60 - tol:
        return NAME_TO_HEX['orange']
    elif hue < 120 - tol:
        return NAME_TO_HEX['yellow']
    elif hue < 180 - tol:
        return NAME_TO_HEX['green']
    elif hue < 250 - tol:
        return NAME_TO_HEX['cyan']
    elif hue < 280 - tol:
        return NAME_TO_HEX['blue']
    elif hue < 325 - tol:
        return NAME_TO_HEX['purple']
    else:
        return NAME_TO_HEX['pink']

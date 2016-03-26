def hue_to_hex(hue):
    if hue < 36:
        # red
        return '#ff0000'
    elif hue < 60:
        # orange
        return '#ff9900'
    elif hue < 120:
        # yellow
        return '#ffff00'
    elif hue < 180:
        # green
        return '#00ff00'
    elif hue < 250:
        # cyan
        return '#00ffff'
    elif hue < 280:
        # blue
        return '#0000ff'
    elif hue < 325:
        # purple
        return '#9900ff'
    else:
        # pink
        return '#ff00ff'

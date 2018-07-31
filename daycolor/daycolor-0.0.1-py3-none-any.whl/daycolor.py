"""
# daycolor

daycolor allows you to choose a (RGB) colors for multiple times of the day and 
fluidly return HSV-interpolated "in-between" colors. The times of the day plus 
the color may be specified in a the daycolordict as shown below.

The daycolordict automagically "wraps around", that means unless desired there will never
be a hard jumps between colors.
"""

import colorsys
import datetime

daycolordict = {
    "01:00":(255,127,80),
    "02:00":(257,34,35),
    "03:00":(126,1,0),
    "04:00":(255,21,149),
    "05:00":(141,0,140),
    "06:00":(27,25,109),
    "07:00":(0,0,254),
    "08:00":(3,239,191),
    "09:00":(0,129,2),
    "10:00":(126,255,0),
    "11:00":(255,244,66),
    "12:00":(253,216,161),
    "13:00":(255,127,80),
    "14:00":(257,34,35),
    "15:00":(126,1,0),
    "16:00":(255,21,149),
    "17:00":(141,0,140),
    "18:00":(27,25,109),
    "19:00":(0,0,254),
    "20:00":(3,239,191),
    "21:00":(0,129,2),
    "22:00":(126,255,0),
    "23:00":(255,244,66),
    "23:59":(253,261,161)
    }




def time_to_float(datetimeobject, totalturn=24, minimum=0.0, maximum=1.0):
    """
    Function that returns a float between minimum
    and maximum for a moment within totalturn hours (default: 24)
    00:00 (Midnight) returns a value of 0, 12:00 (Midday) a value of 0.5
    """
    micro = datetimeobject.microsecond / 1000000.
    sec = datetimeobject.second
    minutes = datetimeobject.minute * 60
    hours = datetimeobject.hour%totalturn * 60 * 60
    currentsecond = hours + minutes + sec + micro
    return minimum + currentsecond/86400. * float(maximum)



def daycolordict_to_range(daycolordict, minimum=0.0, maximum=1.0, pattern='%H:%M'):
    """
    Converts a dict with time indices from "00:00" to "24:00"
    to a dict with a range based index between minimum and maximum
    """
    minimum = float(minimum)
    maximum = float(maximum)
    # Create a new dict and parse each key and convert to float
    # E.g. "00:00" is 0.0, "12:00" is 0.5 and "24:00" is 1.0
    newdict = {}
    for key in daycolordict.keys():
        time = datetime.datetime.strptime(key, pattern)
        newkey = time_to_float(time, 24, minimum, maximum)
        newdict[newkey] = daycolordict[key]
    # Check if minimum or maximum exist as key value, if not
    # set to a interpolated inbetween value
    if not minimum in newdict or maximum in newdict:
        maxkey = max(newdict)
        minkey = min(newdict)
        distance = maxkey - minkey
        interpolatedvalue = lerp3d(distance, newdict[minkey], newdict[maxkey], minimum, maximum)
        newdict[minimum] = interpolatedvalue
        newdict[maximum] = interpolatedvalue
    if not minimum in newdict:
        newdict[minimum] = newdict[maximum]
    if not maximum in newdict:
        newdict[maximum] = newdict[minimum]
    return newdict



def mapvalue(value, leftMin, leftMax, rightMin=0.0, rightMax=1.0):
    """
    map a value between two ranges
    """
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)



def lerp(value, start, end, minimum=0.0, maximum=1.0):
    """
    Linear Interpolation between two points
    """
    value = float(value)
    start = float(start)
    end = float(end)
    return minimum+((1.0-value) * start +value * end)*maximum

def circularlerp(value, start, end):
    """
    Circular Lerp interpolation
    Wraps around to get closest path (0.0 = 1.0)
    """
    shortest_path = ((end-start)+0.5)%1.0 -0.5
    result = (start+shortest_path*value)%1.0
    return result


def lerp3d(value, start, end, minimum=0.0, maximum=1.0):
    """
    3D Linear Interpolation
    """
    r1 = lerp(value, start[0], end[0], minimum, maximum)
    r2 = lerp(value, start[1], end[1], minimum, maximum)
    r3 = lerp(value, start[2], end[2], minimum, maximum)
    return (r1, r2, r3)


def lerphsv(value, start, end, minimum=0.0, maximum=1.0):
    """
    HSV Linear Interpolation (Hue takes closest path)
    """
    h = circularlerp(value, start[0], end[0])
    s = lerp(value, start[1], end[1], minimum, maximum)
    v = lerp(value, start[2], end[2], minimum, maximum)
    return (h, s, v)


def interpolate_table(floatdict, value, minimum=0.0, maximum=1.0):
    """
    Select two table values based on a value and interpolate between them
    """
    # Clip value if it overflows
    if value > maximum: value = maximum
    if value < minimum: value = minimum
    floatkeys = sorted(floatdict)
    # Find out positive and negative distances for each key
    posdistances = {}
    negdistances = {}
    for i, key in enumerate(floatkeys):
        posdistance = value-key
        negdistance = key-value
        # Discard negative distances
        if not posdistance < 0:
            posdistances[key] = posdistance
        if not negdistance < 0:
            negdistances[key] = negdistance
    # Find the float keys with the two closest values (up and down)
    closestkeydown = min(posdistances, key=posdistances.get)
    closestkeyup = min(negdistances, key=negdistances.get)
    # Only interpolate if we are not directly on a value
    if not closestkeyup == closestkeydown:
        # Return a value btw. 0.0 and 1.0 representing the distance
        inbetweenvalue = mapvalue(value, closestkeydown, closestkeyup, 0.0, 1.0)
        # Interpolate between the two closest values
        output = lerphsv(inbetweenvalue, floatdict[closestkeydown], floatdict[closestkeyup])
        blendvalue = inbetweenvalue
    else:
        output = floatdict[closestkeyup]
        blendvalue = 1.0
    # Return interpolated  last value, next value and blendvalue
    return output[0], output[1], output[2], closestkeydown, closestkeyup, blendvalue


def get_by_value(value, daycolordict, minimum=0.0, maximum=1.0, pattern='%H:%M'):
    """
    Returns a list of 3 color values, the values for the last for a
    value between 0.0 and 1.0, HSV interpolation
    """
    # Create a dict with float keys (0.0 to 1.0) from time based dict
    floatdict = daycolordict_to_range(daycolordict, minimum, maximum, pattern)
    # Convert all RGB values in dict to HSV color space for more
    # natural color interpolation
    hsvtable = {}
    for key in floatdict.keys():
        r, g, b = floatdict[key]
        r, g, b = r/255., g/255., b/255.
        hsvtable[key] = colorsys.rgb_to_hsv(r, g, b)
    # Get the interpolated HSV value
    h, s, v, lastkey, nextkey, blendvalue = interpolate_table(hsvtable, value)
    # Covnert it back to RGB for convinience
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = r*255, g*255, b*255
    return (r, g, b)


def get_by_datetime(datetimeobject, daycolordict, pattern='%H:%M'):
	"""
	Returns the interpolated color value for a given datetime
	"""
	value = time_to_float(datetimeobject)
	return get_by_value(value, daycolordict, pattern=pattern)


def get_current(daycolordict, pattern='%H:%M'):
	"""
	Returns the interpolated color value for the current moment
	"""
	now = datetime.datetime.now()
	return get_by_datetime(now, daycolordict, pattern=pattern)



if __name__ == "__main__":
    # Main is only used for debugging
    r, g, b = get_current(daycolordict)
    print("Current color:".ljust(23)+str((int(r), int(g), int(b))))
    import random
    print(get_by_value(random.random(), daycolordict))

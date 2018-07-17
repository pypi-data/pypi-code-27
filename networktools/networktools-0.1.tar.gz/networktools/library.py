import uuid
import shlex
import simplejson as json
import datetime

def my_random_string(string_length=10):
    """Returns a random string of length string_length.

    :param string_length: a positive int value to define the random length
    :return:
    """
    a = 3
    assert string_length >= a, "No es un valor positivo sobre " + str(a)
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.
# str(my_random_string(6))
# print(my_random_string(6)) # For example, D9E50C


def fill_pattern(var_list, pattern):
    """
    Replace values in pattern
    var_list has to have 'pattern' and 'value' keys
    pattern is a string with some keys inside
    """
    code = pattern
    for lista in var_list:
        keys = lista.keys()
        # print(lista)
        assert 'pattern' in keys and 'value' \
            in keys, "Lista incorrecta en " + str(lista)
        code = code.replace(lista['pattern'], lista['value'])
    # print(code)
    return code


def pattern_value(pattern_str, val):
    "Return a specific dictionary with keys pattern and value"
    return dict(pattern=pattern_str, value=val)

def key_on_dict(key, mydict):
    if key in mydict:
        if mydict[key]:
            return True
        else:
            return False
    else:
        return False

def check_gsof(mydict):
    return key_on_dict('ECEF', mydict) and key_on_dict('POSITION_VCV', mydict)

def gns_dumps(string, char='#'):
    a = json.dumps(string)
    b = a.replace('\"', char)
    q=3*char
    c = b.replace('\\#','$%s' %q)
    return c


def gns_loads(string, char='#'):
    q=3*char
    a=string.replace('$%s' %q,'\\#')
    b = a.replace(char, '\"')
    c = json.loads(b)
    return c


def context_split(value, separator='|'):
    """
    Split and take care of \"\"
    """
    print("Context split")
    print(value)
    try:
        q = shlex.shlex(value, posix=True)
        q.whitespace += separator
        q.whitespace_split = True
        q.quotes = '\"'
        q_list = list(q)
        return q_list
    except Exception as e:
        print("Error en separación de contexto %s" %e)
        raise e


def geojson2angularjson(content):
    """
    content is a GeoJson object must be converted to a Angular Chart JSON object....
    """

    dt=datetime.utcfromtimestamp(int(content['properties']['time'])/1000)
    new_value=dict(
        source="DataWork",
        station_name=content['properties']['station'],
        timestamp=dt,
        data={
            'N':{
            'value':content['features'][0]['geometry']['coordinates'][0],
            'error':content['properties']['NError'],
            'min':content['features'][0]['geometry']['coordinates'][0]-content['properties']['NError'],
            'max':content['features'][0]['geometry']['coordinates'][0]+content['properties']['NError']
        },
              'E':{
            'value':content['features'][0]['geometry']['coordinates'][1],
            'error':content['properties']['EError'],
            'min':content['features'][0]['geometry']['coordinates'][1]-content['properties']['EError'],
            'max':content['features'][0]['geometry']['coordinates'][1]+content['properties']['EError']

              },
              'U':{
            'value':content['features'][0]['geometry']['coordinates'][2],
            'error':content['properties']['UError'],
            'min':content['features'][0]['geometry']['coordinates'][2]-content['properties']['UError'],
            'max':content['features'][0]['geometry']['coordinates'][2]+content['properties']['UError']
          },
            }
        #last_update=datetime.utcnow()
        )

    return data

import rethinkdb as r

def geojson2rethinkjson(content):
    """
    content is a GeoJson object must be converted to a RethinkDB JSON object....
    """

    try:
        #print("Content...:%s"%content['properties'])
        time=content['properties']['time']
        dt0=content['properties']['dt']
        #print("Datetime Original %s" %dt0)
        c_datetime=dt0.isoformat()
        #print("Fecha y tiempo %s" %dt0.isoformat())
        dt=r.iso8601(dt0.isoformat())
        dt_gen=content['properties']['DT_GEN']
    except Exception as exec:
        print("Error en calcular fecha tiempo %s" %exec)
        raise exec
    new_value=dict(
        source="DataWork",
        station_name=content['properties']['station'],
        DT_GEN=dt_gen,
        timestamp=time,
        data={
            'N':{
            'value':content['features'][0]['geometry']['coordinates'][0],
            'error':content['properties']['NError'],
            'min':content['features'][0]['geometry']['coordinates'][0]-content['properties']['NError'],
            'max':content['features'][0]['geometry']['coordinates'][0]+content['properties']['NError']
        },
              'E':{
            'value':content['features'][0]['geometry']['coordinates'][1],
            'error':content['properties']['EError'],
            'min':content['features'][0]['geometry']['coordinates'][1]-content['properties']['EError'],
            'max':content['features'][0]['geometry']['coordinates'][1]+content['properties']['EError']

              },
              'U':{
            'value':content['features'][0]['geometry']['coordinates'][2],
            'error':content['properties']['UError'],
            'min':content['features'][0]['geometry']['coordinates'][2]-content['properties']['UError'],
            'max':content['features'][0]['geometry']['coordinates'][2]+content['properties']['UError']
          },
            }
        #last_update=datetime.utcnow()
        )

    return new_value


def geojson2json(content):
    """
    content is a GeoJson object must be converted to a RethinkDB JSON object....
    """

    try:
        #print("Content...:%s"%content['properties'])
        time=content['properties']['time']
        dt0=content['properties']['dt']
        #print("Datetime Original %s" %dt0)
        c_datetime=dt0.isoformat()
        #print("Fecha y tiempo %s" %dt0.isoformat())
        dt=dt0.isoformat()
        dt_gen=content['properties']['DT_GEN'].isoformat()
    except Exception as exec:
        print("Error en calcular fecha tiempo %s" %exec)
        raise exec
    new_value=dict(
        source="DataWork",
        station_name=content['properties']['station'],
        DT_GEN=dt_gen,
        timestamp=time,
        data={
            'N':{
            'value':content['features'][0]['geometry']['coordinates'][0],
            'error':content['properties']['NError'],
            'min':content['features'][0]['geometry']['coordinates'][0]-content['properties']['NError'],
            'max':content['features'][0]['geometry']['coordinates'][0]+content['properties']['NError']
        },
              'E':{
            'value':content['features'][0]['geometry']['coordinates'][1],
            'error':content['properties']['EError'],
            'min':content['features'][0]['geometry']['coordinates'][1]-content['properties']['EError'],
            'max':content['features'][0]['geometry']['coordinates'][1]+content['properties']['EError']

              },
              'U':{
            'value':content['features'][0]['geometry']['coordinates'][2],
            'error':content['properties']['UError'],
            'min':content['features'][0]['geometry']['coordinates'][2]-content['properties']['UError'],
            'max':content['features'][0]['geometry']['coordinates'][2]+content['properties']['UError']
          },
            }
        #last_update=datetime.utcnow()
        )

    return new_value

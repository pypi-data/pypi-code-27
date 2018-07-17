from datetime import datetime, timedelta
from datetime import timezone
import pytz

def timestamp():
    return datetime.now(tz=timezone.utc).timestamp()

def now():
    this_tz=pytz.timezone('UTC')
    now=datetime.now(tz=this_tz).astimezone(tz=this_tz)
    return now

def gps_week2time(week, time_week):
    #start date
    try:
        this_tz=pytz.timezone('UTC')
        start_data=datetime(1980,1,6, tzinfo=this_tz).astimezone(tz=this_tz)
    except Exception as exec:
        print("Error en generar start_date %s" %exec)
        raise exec
        # how many weeks and milliseconds after start_date
    delta=timedelta(weeks=week, milliseconds=time_week)
    final_date=start_data+delta
    return final_date

def gps_time(data):
    final_date=datetime.utcnow()
    if 'UTC' in data.keys():
        utc=data['UTC']
        time_week=utc['GPS_MS_OF_WEEK']
        week=utc['GPS_WEEK']
        offset=utc['UTC_OFFSET']
        offset_time=timedelta(seconds=-offset)
        final_date=gps_week2time(week, time_week)+offset_time
        #print("UTC TIME %s" %final_date)
    elif 'TIME' in data.keys():
        LEAP=18
        time=data['TIME']
        GPS_WEEK=time['GPS_WEEK']
        GPS_TIME=time['GPS_TIME']#miliseconds
        try:
            #print("TIME %s" %time)
            pass
        except Exception as exec:
            print("Error en calculo del tiempo %s" %exec)
            raise exec

        offset_time=timedelta(seconds=-LEAP)
        final_date=gps_week2time(GPS_WEEK, GPS_TIME)+offset_time
        #print("GPS TIME %s" %final_date)
    return final_date


def get_datetime_di(delta:int=600):
    df=datetime.now(tz=pytz.utc)
    di=df+timedelta(seconds=-delta)
    return di.astimezone(tz=pytz.utc).isoformat()

# -*- coding: utf-8 -*-
"""
BART API wrapper for Python 3+

This wrapper's main purpose is to display (print) relevant information
associated with each of the Bart API's amenities, so don't expect too
many methods to return a value (as they'll probably print it instead)!

BART API Documentation: https://api.bart.gov/docs/overview/index.aspx
"""

import requests

__author__ = "Luis Ulloa"


class Bart:
    """
    ----- Bart API -----
    bart = Bart(key)  # key is optional, defaults to universal BART API key


    Advisories
    -----------
    bsa(orig)
    train_count()
    elev()
    elev_help()


    Real-Time Estimates
    -------------------
    etd(orig, plat, direction)
    etd_help()


    Route Information
    -----------------
    routeinfo(route_num, sched_num, date)
    routes(sched_num, date)
    route_help()


    Schedule Information
    --------------------
    arrive(orig, dest time, b, a)
    depart(orig, dest, time, b, a)
    fare(orig, dest, date, sched)
    holiday()
    routesched(route, date, time, sched)
    scheds()
    special()
    stnsched(orig, date)
    sched_help()


    Station Information
    -------------------
    stn_help()
    stninfo(orig)
    stnaccess(orig)
    stns()


    Version Information
    -------------------
    version()


    """
    # links are constants class variables, accessible with Bart.CONSTANT_NAME
    BSA_API_LINK = 'https://api.bart.gov/api/bsa.aspx'       # Advisories
    ETD_API_LINK = 'https://api.bart.gov/api/etd.aspx'       # Real-Time Estimates
    ROUTE_API_LINK = 'https://api.bart.gov/api/route.aspx'   # Route Information
    SCHED_API_LINK = 'https://api.bart.gov/api/sched.aspx'   # Schedule Information
    STN_API_LINK = 'https://api.bart.gov/api/stn.aspx'       # Station Information
    VERS_API_LINK = 'https://api.bart.gov/api/version.aspx'  # Version Information

    def __init__(self, key='MW9S-E7SL-26DU-VV8V'):
        self.key = key

    def bsa(self, orig=None):
        """
        Prints any announcements, if available
        :param orig: ignore this, bsa doesn't support station specific,
                     announcements but will in the future
        """
        cmd = 'bsa'
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'json': 'y'}
        r = requests.get(self.BSA_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            time = data['time']
            date = data['date']
            print("The following announcements were available on %s at %s..." % (date, time))
            bsa = data['bsa']
            for elem in bsa:        # each element is a specific service announcement
                if elem['sms_text']:
                    print("SMS text announcement: %s" % bsa[-1]['sms_text']['#cdata-section'])
                if len(elem['station']) > 0:
                    print("%s: %s" % (elem['station'], elem['description']['#cdata-section']))

    def train_count(self):
        """ Prints/returns count of trains. """
        cmd = 'count'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.BSA_API_LINK, params=payload)
        train_count = 0
        if "error" not in r.text:
            data = r.json()['root']
            train_count = data['traincount']
            print("%s trains active on %s at %s." % (train_count, data['date'], data['time']))
        return train_count

    def elev(self):
        """ Prints elevator announcement details. """
        cmd = 'elev'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.BSA_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            time = data['time']
            date = data['date']
            print("The following announcements were available on %s at %s..." % (date, time))
            bsa = data['bsa']

            for elem in bsa:    # each elem is a service announcement + accompanied sms
                if elem['sms_text']:
                    print("SMS text announcement: %s" % elem['sms_text']['#cdata-section'])

                if len(elem['station']) > 0:
                    print("%s - %s" % (elem['station'], elem['description']['#cdata-section']))

    def elev_help(self):
        """ Prints commands you can use with API. """
        cmd = 'help'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.BSA_API_LINK, params=payload)
        if "error" not in r.text:
            help_msg = r.json()['root']['message']['help']['#cdata-section']
            print(help_msg)
            print("bsa(), train_count(), elev(), elev_help()\n")

    def etd(self, orig, plat=None, direction=None):
        """
        Prints estimated departure time for specified station

        :param orig: specific station, using its abbreviation, ALL for all ETD's
        :param plat: specific platform, ranges b/w 1-4
        :param direction: direction, 'n' north; 's' south

        Note: If orig is 'all', can't use plat or dir. Can't use plat
                and dir together either way (preference plat)
        """
        if plat is not None and direction is not None:  # preference to plat
            direction = None

        cmd = 'etd'
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'plat': plat,
                   'dir': direction, 'json': 'y'}
        r = requests.get(self.ETD_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            date, time = data['date'], data['time']
            print("Estimated departure time(s) for %s on %s %s..." % (orig, date, time))
            if not data.get('station') and data.get('message') != "":
                print(data['message']['warning'])
                return      # nothing matching

            for station in data.get('station'):
                name = station['name']
                print("Departures for %s..." % name)
                for loc in station.get('etd'):
                    dest = loc['destination']
                    print("For those leaving to %s:" % dest)
                    for departure in loc.get('estimate'):
                        minutes = departure['minutes']
                        platform = departure['platform']
                        color = departure['color']
                        direct = departure['direction']
                        print("%s bart on platform %s leaving in %s minutes!" % (color, platform, minutes))
                print()  # spacing b/w each station

    def etd_help(self):
        """ Shows commands for time departure part of api. """
        cmd = 'help'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.ETD_API_LINK, params=payload)
        if "error" not in r.text:
            help_msg = r.json()['root']['message']['help']['#cdata-section']
            print(help_msg)
            print("etd(), etd_help()\n")

    def route_info(self, route_num, sched_num=None, date=None):
        """
        Returns information on a route, can specify schedule number and date as well.

        :param route_num: route number
        :param sched_num: schedule number
        :param date: current date

        Note: don't use schedule and date together, otherwise date is dropped
        """
        cmd = 'routeinfo'
        payload = {'cmd': cmd, 'key': self.key, 'route': route_num, 'sched': sched_num, 'date': date, 'json': 'y'}
        r = requests.get(self.ROUTE_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['routes']['route']
            name, origin, destination, route = data['name'], data['origin'], data['destination'], data['routeID']
            print('%s is %s, going from %s to %s.' % (route, name, origin, destination))

    def routes(self, sched_num=None, date=None):
        """
        Prints routes.

        :param sched_num: schedule number
        :param date: current date

        Note: don't use schedule and date together, otherwise date is dropped
        """
        cmd = 'routes'
        payload = {'cmd': cmd, 'key': self.key, 'sched': sched_num, 'date': date, 'json': 'y'}
        r = requests.get(self.ROUTE_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['routes']
            for route in data['route']:
                name, abbr, route_id = route['name'], route['abbr'], route['routeID']
                print("%s - %s with abbreviation \"%s\"" % (route_id, name, abbr))

    def route_help(self):
        """ prints commands for route (note: "help" refers to this method)"""
        cmd = 'help'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.ROUTE_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['message']['help']['#cdata-section']
            print(data)
            print("route_help(), routes(), route_info()\n")

    def arrive(self, orig, dest, time=None, date=None, b=None, a=None, command="arrive"):
        """
        Requests a trip based on arriving at time specified.

        :param orig: origination station (abbreviation)
        :param dest: destination station (abbreviation)
        :param time: arrival time (defaults to current time) h:mm+am/pm
        :param date: specific date (defaults to today) mm/dd/yy
        :param b: specifies how many trips before specified time should be returned  (0-4, default 2)
        :param a: specifies how many trips after specified time should be returned  (0-4, default 2)
        :param command: used internally, no need to declare this, defaults to arrive
        """
        cmd = command
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'dest': dest, 'time': time,
                   'date': date, 'b': b, 'a': a, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            print("Trips from %s to %s..." % (data['origin'], data['destination']))
            trips = data['schedule']['request']['trip']
            for i in range(0, len(trips), 2):    # each trip has a leg following it
                trip = trips[i]
                # leg = trips[i+1]['leg']   # won't use any data from legs, but know it's here!
                print("Trip from %s to %s on %s with the following fares..."
                      % (trip['@origTimeMin'], trip['@destTimeMin'], trip['@origTimeDate']))
                print("Standard:", trip['@fare'])
                for fare in trip['fares']['fare']:
                    print("%s: %s (%s)" % (fare['@name'], fare['@amount'], fare['@class']))
                print()  # spacing

    def depart(self, orig, dest, time=None, date=None, b=None, a=None):
        """
        Requests a trip based on departing at specified time. Calls arrive
        but specifies depart as command, same data output format.

        :param orig: origination station (abbreviation)
        :param dest: destination station (abbreviation)
        :param time: departure time for trip h:mm+am/pm
        :param date: specific date (defaults to today) mm/dd/yy
        :param b: specifies how many trips before specified time should be returned  (0-4, default 2)
        :param a: specifies how many trips after specified time should be returned  (0-4, default 2)
        """
        self.arrive(orig, dest, time, date, b, a, "depart")

    def fare(self, orig, dest, date=None, sched=None):
        """
        Requests the fare information for a trip between two stations.

        :param orig: origination station (abbreviation)
        :param dest: destination station (abbreviation)
        :param date: specific date mm/dd/yyyy, current date default
        :param sched: specific schedule to use (optional)
        """
        cmd = 'fare'
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'dest': dest, 'date': date, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            print("A trip from %s to %s has the following fare..." % (data['origin'], data['destination']))
            for fare in data['fares']['fare']:
                print("%s for %s (%s)" % (fare['@amount'], fare['@name'], fare['@class']))

    def holiday(self):
        """ Prints BART schedule type for any holiday. """
        cmd = 'holiday'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['holidays'][0]
            for hday in data['holiday']:
                name, date, sched_type = hday['name'], hday['date'], hday['schedule_type']
                print("%s on %s has a %s schedule type." % (name, date, sched_type))

    def routesched(self, route, date=None, time=None, sched=None):
        """
        Prints detailed schedule information for a specific route.

        :param route: specifies a route information to return
        :param date: specifies which date mm/dd/yyyy (defaults to today)
        :param time: specifies what time to use hh:mm tt (defaults to now)
        :param sched: specifies schedule to use (defaults to current schedule)
        """
        cmd = 'routesched'
        payload = {'cmd': cmd, 'key': self.key, 'route': route, 'time': time,
                   'date': date, 'sched': sched, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            print("For schedule number %s on %s..." % (data['sched_num'], data['date']))
            for path in data['route']['train']:
                stops = ', '.join([loc['@station'] + "(" + loc["@origTime"] + ")"
                                   for loc in path['stop'] if loc.get('@origTime')])
                print("Train with ID %s has the following stops: %s" % (path['@trainId'], stops))

    def scheds(self):
        """ Prints schedule id's and effective dates. """
        cmd = 'scheds'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        data = r.json()['root']['schedules']
        for sched in data['schedule']:
            print("Schedule %s has effective date %s" % (sched['@id'], sched['@effectivedate']))

    def special(self):
        """ Prints information about current and upcoming BART special schedules. """
        cmd = 'special'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['special_schedules']
            for spec in data['special_schedule']:
                print("From %s to %s: %s" %
                      (spec['start_date'], spec['end_date'], spec['text']['#cdata-section']))
                print("The routes affect are %s, more information here: %s" %
                      (spec['routes_affected'], spec['link']['#cdata-section']))

    def stnsched(self, orig, date=None):
        """
        Requests detailed schedule information for a specific schedule.

        :param orig: station for which schedule is requested
        :param date: specifies date to use mm/dd/yy (default today)
        """
        cmd = 'stnsched'
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'date': date, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            print("%s schedule (%s) details on %s..." %
                  (data['station']['name'], data['sched_num'], data['date']))
            for route in data['station']['item']:
                print("Train %s with %s, (Head Station %s): from %s to %s." %
                      (route['@trainId'], route['@line'], route['@trainHeadStation'],
                       route['@origTime'], route['@destTime']))

    def sched_help(self):
        """ Shows commands for time departure part of api. """
        cmd = 'help'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.SCHED_API_LINK, params=payload)
        if "error" not in r.text:
            help_msg = r.json()['root']['message']['help']['#cdata-section']
            print(help_msg)
            print("arrive(), depart(), fare(), sched_help(), holiday(), routesched(), scheds(), special(), stnsched()\n")

    def stninfo(self, orig):
        """
        Prints detailed information on specified station.
        Specifically, station name, full address, link to website,
        The data returned could also be used to show north and south routes
        and platforms, but this function doesn't show that.

        :param orig: abbreviated name of target station
        """
        cmd = 'stninfo'
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'json': 'y'}
        r = requests.get(self.STN_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['stations']['station']
            name = data['name']
            address, city, state, zipcode = data['address'], data['city'], data['state'], data['zipcode']
            link = data['link']['#cdata-section']
            print("%s is at %s, %s, %s %s and can be found at %s." % (name, address, city, state, zipcode, link))

    def stns(self):
        """ Provides list of BART stations with their abbreviations, full names, and addresses. """
        cmd = 'stns'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.STN_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            for station in data['stations']['station']:
                name = station['name']
                abbr = station['abbr']
                address, city, state, zipc = station['address'], station['city'], station['state'], station['zipcode']
                print("%s (\"%s\") is at %s, %s, %s %s." % (name, abbr, address, city, state, zipc))

    def stnaccess(self, orig):
        """
        Displays access/neighborhood info for specified station.
        Showing the "legend" means showing what each flag in data stands
        for; won't be using that here.

        This function will report if it has parking/bike/bike_station/lockers,
        as well as the associated message.

        :param orig: target station (use abbreviation)
        """
        cmd = 'stnaccess'
        payload = {'cmd': cmd, 'key': self.key, 'orig': orig, 'json': 'y'}
        r = requests.get(self.STN_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']['stations']['station']
            parking, bike, bike_station, lockers = data['@parking_flag'],data['@bike_flag'],\
                data['@bike_station_flag'], data['@locker_flag']

            print("%s: " % data['name'])
            print("Parking:", "yes" if parking == '1' else "no")
            print("Bike Racks:", "yes" if bike == '1' else "no")
            print("Bike Station:", "yes" if bike_station == '1' else "no")
            print("Lockers:",  "yes" if lockers == '1' else "no")

    def stn_help(self):
        """ Shows commands for time departure part of api. """
        cmd = 'help'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.STN_API_LINK, params=payload)
        if "error" not in r.text:
            help_msg = r.json()['root']['message']['help']['#cdata-section']
            print(help_msg)
            print("stn_help(), stninfo(), stnaccess(), stns()\n")

    def version(self):
        """ Prints version details. """
        cmd = 'ver'
        payload = {'cmd': cmd, 'key': self.key, 'json': 'y'}
        r = requests.get(self.VERS_API_LINK, params=payload)
        if "error" not in r.text:
            data = r.json()['root']
            api_version = data['apiVersion']
            api_copyright = data['copyright']
            api_license = data['license']
            print("Version: %s\nCopyright: %s\nLicense: %s\n" % (api_version, api_copyright, api_license))

    def help(self):
        """ Display all help messages. """
        self.route_help()
        self.elev_help()
        self.etd_help()
        self.stn_help()
        self.sched_help()


if __name__ == "__main__":
    # example usage, see test.py for import formatting
    bart = Bart()
    # bart.route_info(1)
    # bart.routes()
    # bart.route_help()
    # bart.bsa()
    # bart.train_count()
    # bart.elev()
    # bart.elev_help()
    # bart.etd('ALL')
    # bart.etd('RICH', plat=2)
    # bart.etd('RICH', direction='s')
    # bart.etd('RICH', plat=2, direction='s')
    # bart.etd_help()
    # bart.version()
    # bart.stninfo('24TH')
    # bart.stns()
    # bart.stnaccess('12th')
    # bart.stn_help()
    # bart.holiday()
    bart.help()
    # bart.arrive("ASHB", "CIVC")
    # bart.depart("ASHB", "CIVC")
    # bart.fare("ASHB", "CIVC")
    # bart.routesched(1)
    # bart.scheds()
    # bart.special()
    # bart.stnsched("ASHB")

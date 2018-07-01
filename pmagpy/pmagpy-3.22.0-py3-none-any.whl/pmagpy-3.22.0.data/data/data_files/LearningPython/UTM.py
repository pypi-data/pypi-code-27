#!/usr/bin/env python
# Lat Long-UTM, UTM-Lat Long conversions

from __future__ import division
from __future__ import print_function
from past.utils import old_div
from math import pi, sin, cos, tan, sqrt, radians, degrees

_EquatorialRadius = 2
_eccentricitySquared = 3

_ellipsoid = [
# id, Ellipsoid name, Equatorial Radius, square of eccentricity
# first once is a placeholder only, To allow array indices to match id numbers
        [ 0, "Placeholder", 0.0, 0.0],
        [ 1, "European Datum 1950",    6378388.0000, 0.006723000],
        [ 2, "Airy",                   6377563.3960, 0.006670540],
        [ 3, "Australian National",    6378160.0000, 0.006694542],
        [ 4, "Bessel 1841",            6377397.1550, 0.006674372],
        [ 5, "Clarke 1866",            6378206.4000, 0.006768658],
        [ 6, "Clarke 1880",            6378249.1450, 0.006803511],
        [ 7, "Everest",                6377276.3452, 0.006637847],
        [ 8, "Fischer 1960 (Mercury)", 6378166.0000, 0.006693422],
        [ 9, "Fischer 1968",           6378150.0000, 0.006693422],
        [ 10, "GRS 1967",              6378160.0000, 0.006694605],
        [ 11, "GRS 1980",              6378137.0000, 0.006694380],
        [ 12, "Helmert 1906",          6378200.0000, 0.006693422],
        [ 13, "Hough",                 6378270.0000, 0.006722670],
        [ 14, "International",         6378388.0000, 0.006722670],
        [ 15, "Krassovsky",            6378245.0000, 0.006693422],
        [ 16, "Modified Airy",         6377340.1890, 0.006670540],
        [ 17, "Modified Everest",      6377304.0000, 0.006637847],
        [ 18, "Modified Fischer 1960", 6378155.0000, 0.006693422],
        [ 19, "South American 1969",   6378160.0000, 0.006694542],
        [ 20, "WGS 60",                6378165.0000, 0.006693422],
        [ 21, "WGS 66",                6378145.0000, 0.006694542],
        [ 22, "WGS 72",                6378135.0000, 0.006694318],
        [ 23, "WGS 84",                6378137.0000, 0.006694380]
]

# Reference ellipsoids derived from Peter H. Dana's website-
# http://www.utexas.edu/depts/grg/gcraft/notes/datum/elist.html
# Department of Geography, University of Texas at Austin
# Internet: pdana@mail.utexas.edu
# 3/22/95

# Source
# Defense Mapping Agency. 1987b. DMA Technical Report: Supplement to Department of Defense World Geodetic System
# 1984 Technical Report. Part I and II. Washington, DC: Defense Mapping Agency


def LLtoUTM(ReferenceEllipsoid, Long, Lat, zone = None):
        """
        converts lat/long to UTM coords.  Equations from USGS Bulletin 1532
        East Longitudes are positive, West longitudes are negative
        North latitudes are positive, South latitudes are negative
        Lat and Long are in decimal degrees
        Written by Chuck Gantz- chuck.gantz@globalstar.com
        """

        a = _ellipsoid[ReferenceEllipsoid][_EquatorialRadius]
        eccSquared = _ellipsoid[ReferenceEllipsoid][_eccentricitySquared]
        k0 = 0.9996

# Make sure the longitude is between-180.00 .. 179.9
        LongTemp = (Long+180)-int(old_div((Long+180),360))*360-180 #-180.00 .. 179.9

        LatRad = radians(Lat)
        LongRad = radians(LongTemp)

        if zone is None:
                ZoneNumber = int(old_div((LongTemp+180),6))+1
        else:
                ZoneNumber = zone

        if Lat >= 56.0 and Lat < 64.0 and LongTemp >= 3.0 and LongTemp < 12.0:
                ZoneNumber = 32

        # Special zones for Svalbard
        if Lat >= 72.0 and Lat < 84.0:
                if  LongTemp >= 0.0  and LongTemp <  9.0:ZoneNumber = 31
                elif LongTemp >= 9.0  and LongTemp < 21.0: ZoneNumber = 33
                elif LongTemp >= 21.0 and LongTemp < 33.0: ZoneNumber = 35
                elif LongTemp >= 33.0 and LongTemp < 42.0: ZoneNumber = 37

        LongOrigin = (ZoneNumber-1)*6-180+3 #+3 puts origin in middle of zone
        LongOriginRad = radians(LongOrigin)

        # compute the UTM Zone from the latitude and longitude
        UTMZone = "%d%c" % (ZoneNumber, _UTMLetterDesignator(Lat))

        eccPrimeSquared = old_div((eccSquared),(1-eccSquared))
        N = old_div(a,sqrt(1-eccSquared*sin(LatRad)*sin(LatRad)))
        T = tan(LatRad)*tan(LatRad)
        C = eccPrimeSquared*cos(LatRad)*cos(LatRad)
        A = cos(LatRad)*(LongRad-LongOriginRad)

        M = a*(
                (1-old_div(eccSquared,4)-3*eccSquared*eccSquared/64-5*eccSquared*eccSquared*eccSquared/256)*LatRad
                -(3*eccSquared/8+3*eccSquared*eccSquared/32+45*eccSquared*eccSquared*eccSquared/1024)*sin(2*LatRad)
                +(15*eccSquared*eccSquared/256+45*eccSquared*eccSquared*eccSquared/1024)*sin(4*LatRad)
                -(35*eccSquared*eccSquared*eccSquared/3072)*sin(6*LatRad)
        )

        UTMEasting = (
                k0*N*(A+(1-T+C)*A*A*A/6
                +(5-18*T+T*T+72*C-58*eccPrimeSquared)*A*A*A*A*A/120)
                +500000.0
        )

        UTMNorthing = (k0*(M+N*tan(LatRad)*(
                A*A/2
                +(5-T+9*C+4*C*C)*A*A*A*A/24
                +(61-58*T+T*T+600*C
                -330*eccPrimeSquared
        )*A*A*A*A*A*A/720)))

        if Lat < 0:
                UTMNorthing = UTMNorthing+10000000.0; #10000000 meter offset for southern hemisphere
        return (UTMZone, UTMEasting, UTMNorthing)


def _UTMLetterDesignator(Lat):
        """
        This routine determines the correct UTM letter designator for the given latitude
        returns 'Z' if latitude is outside the UTM limits of 84N to 80S
        Written by Chuck Gantz- chuck.gantz@globalstar.com
        """

        if   84 >= Lat >= 72: return 'X'
        elif 72 >  Lat >= 64: return 'W'
        elif 64 >  Lat >= 56: return 'V'
        elif 56 >  Lat >= 48: return 'U'
        elif 48 >  Lat >= 40: return 'T'
        elif 40 >  Lat >= 32: return 'S'
        elif 32 >  Lat >= 24: return 'R'
        elif 24 >  Lat >= 16: return 'Q'
        elif 16 >  Lat >= 8:  return 'P'
        elif  8 >  Lat >= 0:  return 'N'
        elif  0 >  Lat >=-8:  return 'M'
        elif -8 >  Lat >=-16: return 'L'
        elif -16 > Lat >=-24: return 'K'
        elif -24 > Lat >=-32: return 'J'
        elif -32 > Lat >=-40: return 'H'
        elif -40 > Lat >=-48: return 'G'
        elif -48 > Lat >=-56: return 'F'
        elif -56 > Lat >=-64: return 'E'
        elif -64 > Lat >=-72: return 'D'
        elif -72 > Lat >=-80: return 'C'
        else:                 return 'Z' # if the Latitude is outside the UTM limits

def UTMtoLL(ReferenceEllipsoid, easting, northing, zone):
        """
        converts UTM coords to lat/long.  Equations from USGS Bulletin 1532
        East Longitudes are positive, West longitudes are negative.
        North latitudes are positive, South latitudes are negative
        Lat and Long are in decimal degrees.
        Written by Chuck Gantz- chuck.gantz@globalstar.com
        Converted to Python by Russ Nelson <nelson@crynwr.com>
        """

        k0 = 0.9996
        a = _ellipsoid[ReferenceEllipsoid][_EquatorialRadius]
        eccSquared = _ellipsoid[ReferenceEllipsoid][_eccentricitySquared]
        e1 = old_div((1-sqrt(1-eccSquared)),(1+sqrt(1-eccSquared)))
        #NorthernHemisphere; //1 for northern hemispher, 0 for southern

        x = easting-500000.0 #remove 500,000 meter offset for longitude
        y = northing

        ZoneLetter = zone[-1]
        if ZoneLetter == 'Z':
                raise Exception("Latitude is outside the UTM limits")

        ZoneNumber = int(zone[:-1])
        if ZoneLetter >= 'N':
                NorthernHemisphere = 1  # point is in northern hemisphere
        else:
                NorthernHemisphere = 0  # point is in southern hemisphere
                y-= 10000000.0          # remove 10,000,000 meter offset used for southern hemisphere

        LongOrigin = (ZoneNumber-1)*6-180+3  # +3 puts origin in middle of zone

        eccPrimeSquared = old_div((eccSquared),(1-eccSquared))

        M = old_div(y, k0)
        mu = old_div(M,(a*(1-old_div(eccSquared,4)-3*eccSquared*eccSquared/64-5*eccSquared*eccSquared*eccSquared/256)))

        phi1Rad = (mu+(3*e1/2-27*e1*e1*e1/32)*sin(2*mu)
                  +(21*e1*e1/16-55*e1*e1*e1*e1/32)*sin(4*mu)
                  +(151*e1*e1*e1/96)*sin(6*mu))
        phi1 = degrees(phi1Rad);

        N1 = old_div(a,sqrt(1-eccSquared*sin(phi1Rad)*sin(phi1Rad)))
        T1 = tan(phi1Rad)*tan(phi1Rad)
        C1 = eccPrimeSquared*cos(phi1Rad)*cos(phi1Rad)
        R1 = a*(1-eccSquared)/pow(1-eccSquared*sin(phi1Rad)*sin(phi1Rad), 1.5)
        D = old_div(x,(N1*k0))

        Lat = phi1Rad-(N1*tan(phi1Rad)/R1)*(D*D/2-(5+3*T1+10*C1-4*C1*C1-9*eccPrimeSquared)*D*D*D*D/24
                     +(61+90*T1+298*C1+45*T1*T1-252*eccPrimeSquared-3*C1*C1)*D*D*D*D*D*D/720)
        Lat = degrees(Lat)

        Long = old_div((D-(1+2*T1+C1)*D*D*D/6+(5-2*C1+28*T1-3*C1*C1+8*eccPrimeSquared+24*T1*T1)*D*D*D*D*D/120),cos(phi1Rad))
        Long = LongOrigin+degrees(Long)
        return (Long, Lat)

if __name__ == '__main__':
    (z, e, n) = LLtoUTM(23-1, 3.2, -43.5)
    print(z, e, n)
    print(UTMtoLL(23-1, e, n, z))

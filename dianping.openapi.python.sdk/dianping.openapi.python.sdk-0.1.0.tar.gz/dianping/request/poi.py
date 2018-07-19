from dianping.auth import Sign


class Open_points:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class QueryPoiRequest(Sign):
    open_points = Open_points

    def __init__(self, app_key, app_secret, session, deviceId, user_id=None, city=None, region=None,
                 latitude=None, longitude=None, open_points=None, offset_type=0, radius=20000,
                 category=None, keyword=None, has_coupon=None,
                 has_deal=None, has_online_reservation=None, sort=1, limit=25, page=1,
                 has_hui=None, improve=False, clientType=None):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/querypoi')

        self.set_deviceId(deviceId)
        self.set_user_id(user_id)
        self.set_city(city)
        self.set_region(region)
        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_open_points(open_points)
        self.set_offset_type(offset_type)
        self.set_radius(radius)
        self.set_category(category)
        self.set_keyword(keyword)
        self.set_has_coupon(has_coupon)
        self.set_has_deal(has_deal)
        self.set_has_online_reservation(has_online_reservation)
        self.set_sort(sort)
        self.set_limit(limit)
        self.set_page(page)
        self.set_has_hui(has_hui)
        self.set_improve(improve)
        self.set_clientType(clientType)

    def set_deviceId(self, deviceId):
        self.add_query_param('deviceId', deviceId)

    def set_user_id(self, user_id):
        self.add_query_param('user_id', user_id)

    def set_city(self, city):
        self.add_query_param('city', city)

    def set_region(self, region):
        self.add_query_param('region', region)

    def set_latitude(self, latitude):
        self.add_query_param('latitude', latitude)

    def set_longitude(self, longitude):
        self.add_query_param('longitude', longitude)

    def set_open_points(self, open_points):
        self.add_query_param('open_points', open_points)

    def set_offset_type(self, offset_type):
        self.add_query_param('offset_type', offset_type)

    def set_radius(self, radius):
        self.add_query_param('radius', radius)

    def set_category(self, category):
        self.add_query_param('category', category)

    def set_keyword(self, keyword):
        self.add_query_param('keyword', keyword)

    def set_has_coupon(self, has_coupon):
        self.add_query_param('has_coupon', has_coupon)

    def set_has_deal(self, has_deal):
        self.add_query_param('has_deal', has_deal)

    def set_has_online_reservation(self, has_online_reservation):
        self.add_query_param('has_deal', has_online_reservation)

    def set_sort(self, sort):
        self.add_query_param('sort', sort)

    def set_limit(self, limit):
        self.add_query_param('limit', limit)

    def set_page(self, page):
        self.add_query_param('page', page)

    def set_has_hui(self, has_hui):
        self.add_query_param('has_hui', has_hui)

    def set_improve(self, improve):
        self.add_query_param('improve', improve)

    def set_clientType(self, clientType):
        self.add_query_param('clientType', clientType)


class QueryShopPoiDetailRequest(Sign):
    def __init__(self, app_key, app_secret, session, deviceId, user_id, latitude, longitude, utmSource, utmMedium,
                 business_id=0, offset_type=0, clientType=None):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/querypoidetail')

        self.set_deviceId(deviceId)
        self.set_user_id(user_id)
        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_offset_type(offset_type)

        self.set_utmSource(utmSource)
        self.set_utmMedium(utmMedium)
        self.set_business_id(business_id)
        self.set_clientType(clientType)

    def set_deviceId(self, deviceId):
        self.add_query_param('deviceId', deviceId)

    def set_user_id(self, user_id):
        self.add_query_param('user_id', user_id)

    def set_latitude(self, latitude):
        self.add_query_param('latitude', latitude)

    def set_longitude(self, longitude):
        self.add_query_param('longitude', longitude)

    def set_offset_type(self, offset_type):
        self.add_query_param('offset_type', offset_type)

    def set_utmSource(self, utmSource):
        self.add_query_param('utmSource', utmSource)

    def set_utmMedium(self, utmMedium):
        self.add_query_param('utmMedium', utmMedium)

    def set_business_id(self, business_id):
        self.add_query_param('business_id', business_id)

    def set_clientType(self, clientType):
        self.add_query_param('clientType', clientType)


class QueryCitysRequest(Sign):
    def __init__(self, app_key, app_secret, session):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/querycitys')


class QueryRegionsRequest(Sign):
    def __init__(self, app_key, app_secret, session, city_name=None):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryregions')

        self.set_city_name(city_name)

    def set_city_name(self, city_name):
        self.add_query_param('city_name', city_name)


class QueryCategoriesRequest(Sign):
    def __init__(self, app_key, app_secret, session, city_name):
        Sign.__init__(self)

        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/querycategories')

        self.set_city_name(city_name)

    def set_city_name(self, city_name):
        self.add_query_param('city_name', city_name)


class QueryOverSeasCitiesRequest(Sign):
    def __init__(self, app_key, app_secret, session):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryOverSeasCities')


class QueryHomeProvincesRequest(Sign):
    def __init__(self, app_key, app_secret, session):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryHomeProvinces')


class QueryOverseasProvinces(Sign):
    def __init__(self, app_key, app_secret, session):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryOverseasProvinces')


class QueryCitiesByProvinceNameRequest(Sign):
    def __init__(self, app_key, app_secret, session, province_name):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryCitiesByProvinceName')
        self.set_province_name(province_name)

    def set_province_name(self, province_name):
        self.add_query_param('province_name', province_name)


class QueryPoiBusinessDistrictRequest(Sign):
    def __init__(self, app_key, app_secret, session, city_name):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryPoiBusinessDistrict')
        self.set_city_name(city_name)

    def set_city_name(self, city_name):
        self.add_query_param('city_name', city_name)


class QueryOpenCategoryNameRequest(Sign):
    def __init__(self, app_key, app_secret, session, city_name):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryOpenCategoryName')
        self.set_city_name(city_name)

    def set_city_name(self, city_name):
        self.add_query_param('city_name', city_name)


class QueryCityByCoordinate(Sign):
    def __init__(self, app_key, app_secret, session, latitude, longitude, coordType):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/querycitybycoordinate')
        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_coordType(coordType)

    def set_latitude(self, latitude):
        self.add_query_param('latitude', latitude)

    def set_longitude(self, longitude):
        self.add_query_param('longitude', longitude)

    def set_coordType(self, coordType):
        self.add_query_param('coordType', coordType)


class QueryShopSearchUrl(Sign):
    def __init__(self, app_key, app_secret, session, cityname, platform=None, regionname=None, categoryname=None, keyword=None, sorttype=None):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/queryshopsearchurl')
        self.set_cityname(cityname)
        self.set_platform(platform)
        self.set_regionname(regionname)
        self.set_categoryname(categoryname)
        self.set_keyword(keyword)
        self.set_sorttype(sorttype)

    def set_cityname(self, cityname):
        self.add_query_param('cityname', cityname)

    def set_platform(self, platform):
        self.add_query_param('platform', platform)

    def set_regionname(self, regionname):
        self.add_query_param('regionname', regionname)

    def set_categoryname(self, categoryname):
        self.add_query_param('categoryname', categoryname)

    def set_keyword(self, keyword):
        self.add_query_param('keyword', keyword)

    def set_sorttype(self, sorttype):
        self.add_query_param('sorttype', sorttype)


class BatchQueryPoiDetailRequest(Sign):
    def __init__(self, app_key, app_secret, session, deviceId, user_id, latitude, longitude, utmSource, utmMedium,
                 openShopIds, offset_type=0, clientType=None):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/batchquerypoidetail')

        self.set_deviceId(deviceId)
        self.set_user_id(user_id)
        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_offset_type(offset_type)

        self.set_utmSource(utmSource)
        self.set_utmMedium(utmMedium)
        self.set_openShopIds(openShopIds)
        self.set_clientType(clientType)

    def set_deviceId(self, deviceId):
        self.add_query_param('deviceId', deviceId)

    def set_user_id(self, user_id):
        self.add_query_param('user_id', user_id)

    def set_latitude(self, latitude):
        self.add_query_param('latitude', latitude)

    def set_longitude(self, longitude):
        self.add_query_param('longitude', longitude)

    def set_offset_type(self, offset_type):
        self.add_query_param('offset_type', offset_type)

    def set_utmSource(self, utmSource):
        self.add_query_param('utmSource', utmSource)

    def set_utmMedium(self, utmMedium):
        self.add_query_param('utmMedium', utmMedium)

    def set_openShopIds(self, openShopIds):
        self.add_query_param('openShopIds', openShopIds)

    def set_clientType(self, clientType):
        self.add_query_param('clientType', clientType)


class PoiDetailRequest(Sign):
    def __init__(self, app_key, app_secret, session, deviceId, user_id, latitude, longitude, utmSource, utmMedium,
                 openShopId, offset_type=0, clientType=None):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod("GET")
        self.set_url('https://openapi.dianping.com/router/poi/poidetail')

        self.set_deviceId(deviceId)
        self.set_user_id(user_id)
        self.set_latitude(latitude)
        self.set_longitude(longitude)
        self.set_offset_type(offset_type)

        self.set_utmSource(utmSource)
        self.set_utmMedium(utmMedium)
        self.set_openShopId(openShopId)
        self.set_clientType(clientType)

    def set_deviceId(self, deviceId):
        self.add_query_param('deviceId', deviceId)

    def set_user_id(self, user_id):
        self.add_query_param('user_id', user_id)

    def set_latitude(self, latitude):
        self.add_query_param('latitude', latitude)

    def set_longitude(self, longitude):
        self.add_query_param('longitude', longitude)

    def set_offset_type(self, offset_type):
        self.add_query_param('offset_type', offset_type)

    def set_utmSource(self, utmSource):
        self.add_query_param('utmSource', utmSource)

    def set_utmMedium(self, utmMedium):
        self.add_query_param('utmMedium', utmMedium)

    def set_openShopId(self, openShopId):
        self.add_query_param('openShopId', openShopId)

    def set_clientType(self, clientType):
        self.add_query_param('clientType', clientType)
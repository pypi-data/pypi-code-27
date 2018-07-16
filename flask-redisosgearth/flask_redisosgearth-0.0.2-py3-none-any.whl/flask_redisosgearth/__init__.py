import redis
from flask import current_app

class Service(object):
    def __init__(self, app=None, strict=True, key_prefix=None, *args, **kwargs):
        self.__redis = redis.StrictRedis if strict else redis.Redis
        self.__redis_kwargs = kwargs
        self.key_prefix = key_prefix or ''

        if app is not None:
            self.init_app(app)

    def init_app(self, app, *args, **kwargs):
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        self.__redis_kwargs.update(kwargs)
        self.__redis_client = self.__redis.from_url(redis_url, **self.__redis_kwargs)

    def addcell(self, dct):
        lua = """
            self.__redis.call('HMSET', KEYS[1], ARGV[1], ARGV[2], ARGV[3], ARGV[4], ARGV[5], ARGV[6], ARGV[7], 
            ARGV[8], ARGV[9], ARGV[10], ARGV[11], ARGV[12], ARGV[13], ARGV[14], ARGV[15], ARGV[16], ARGV[17], 
            ARGV[18], ARGV[19], ARGV[20])"""
        cell = dct['cell']
        city = dct['city'] 
        weather = dct['weather']
        people = dct['people']
        like = dct['like']
        movement = dct['movement']
        lon = dct['lon']
        lat = dct['lat']
        height = dct['height']
        level = dct['level']
        relationships = dct['relationships']
        multiply = self.__redis.register_script(lua)
        multiply(keys=[cell], args=['city', city, 'weather', weather, 'people', people, 'like', like, 
            'movement', movement, 'lon', lon, 'lat', lat, 'height', height, 'level', level, 'relationships', relationships], 
                client=self.flask_redis) 
         
    def getcell(self, key):
        lua = """
            local rlt = self.__redis.call('HMGET', KEYS[1], ARGV[1], ARGV[2], ARGV[3], ARGV[4], ARGV[5], ARGV[6], ARGV[7], 
                ARGV[8], ARGV[9], ARGV[10])
            return rlt"""
        multiply = self.__redis.register_script(lua)
        rlt = multiply(keys=[key], args=['city', 'weather', 'people', 'like', 'movement', 'lon', 'lat', 'height', 'level', 
            'relationships'], client=self.flask_redis)
        return rlt

    def delcell(self, key):
        lua = """
            local rlt = self.__redis.call('DEL', KEYS[1])
            return rlt"""
        multiply = self.__redis.register_script(lua)
        rlt = multiply(keys=[key], client=self.flask_redis)
        return rlt

    def iskeyexists(self, key):
        lua = """
            local rlt = self.__redis.call('EXISTS', KEYS[1])
            return rlt"""
        multiply = self.__redis.register_script(lua)
        rlt = multiply(keys=[key], client=self.flask_redis)
        return rlt

import redis
import datetime

from typing import Optional

STATS_PREFIX = "STATS"
SEP = "_"

def incrStat(statName: str, redisConnection: redis.StrictRedis = None) -> None:
    if not redisConnection:
        redisConnection = redis.StrictRedis('redis')
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    redisConnection.incr(STATS_PREFIX + SEP + statName + SEP + date)

def getStatToday(statName: str, redisConnection: redis.StrictRedis = None) -> Optional[int]:
    if not redisConnection:
        redisConnection = redis.StrictRedis('redis')
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    ret = redisConnection.get(STATS_PREFIX + SEP + statName + SEP + date)
    if ret:
        return int(ret)
    else:
        return None
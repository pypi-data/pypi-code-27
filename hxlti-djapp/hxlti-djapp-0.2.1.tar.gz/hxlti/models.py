import logging
from datetime import datetime
from datetime import timedelta
import pytz
from uuid import uuid4

from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import Model



def expire_in_weeks(ttl=24):
    return datetime.now(pytz.utc) + timedelta(weeks=ttl)


def generate_id():
    return str(uuid4())


class Consumer(Model):
    created = DateTimeField(auto_now_add=True, null=False)
    modified = DateTimeField(auto_now=True, null=False)
    consumer = CharField(max_length=128, primary_key=True, default=generate_id)
    secret_key = CharField(max_length=128, default=generate_id)
    expire_on = DateTimeField(default=expire_in_weeks)


    def has_expired(self, now=None):
        if now is None:
            now = datetime.now(pytz.utc)
        return self.expire_on < now

    def __repr__(self):
        return self.consumer

    def __str__(self):
        return self.__repr__()





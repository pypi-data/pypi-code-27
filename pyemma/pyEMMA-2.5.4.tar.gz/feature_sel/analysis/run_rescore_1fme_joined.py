# coding: utf-8

from celery import group
import rescore_1FME_joined as c
tasks = group([c.run.s(i) for i in range(0, 14)])
tasks.apply_async()

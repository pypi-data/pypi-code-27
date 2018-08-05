#!/usr/bin/python3
# encoding: utf-8
from datetime import datetime, timedelta

from pymongo import MongoClient, errors


class MogoQueue():

    OUTSTANDING = 1  # 初始状态
    PROCESSING = 2  # 正在下载状态
    COMPLETE = 3  # 下载完成状态
    ERROR = 4

    def __init__(self, db, collection, timeout=300):  # 初始mongodb连接
        self.client = MongoClient()
        self.Client = self.client[db]
        self.db = self.Client[collection]
        self.timeout = timeout
        self.daytime = 86400

    def __bool__(self):
        record = self.db.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push_url(self, url, title=None, root=None):  # 这个函数用来添加新的URL进队列
        try:
            self.db.insert(
                {'_id': url, 'status': self.OUTSTANDING, 'title': title, 'from': root})
            print(url, 'insert successfully')
        except errors.DuplicateKeyError as e:  # 报错则代表已经存在于队列之中了
            print(url, 'already exists')

    def push_imgurl(self, title, url):
        try:
            self.db.insert(
                {'_id': title, 'statue': self.OUTSTANDING, 'url': url})
            print(r'insert successfully')
        except errors.DuplicateKeyError as e:
            print(r'already exists')

    def push_data(self, item):
        try:
            self.db.insert(item)
            print(r'insert successfully')
        except errors.DuplicateKeyError as e:
            print(r'already exists')

    def pop_data(self):
        record = self.db.find(query={
            'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.daytime)},
        })
        if record:
            return record

    def pop_url(self):
        record = self.db.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={
                '$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        record = self.db.find_one({'_id': url})
        if record:
            return record['title']

    def peek(self):
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']
#         else:
#             return None

    def error(self, url):
        self.db.update({'_id': url}, {'$set': {'status': self.ERROR}})

    def complete(self, url):
        self.db.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        record = self.db.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('reset state:', record['_id'])

    def clear(self):
        '''删库'''
        self.db.drop()

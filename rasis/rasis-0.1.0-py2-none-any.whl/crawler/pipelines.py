# -*- coding: utf-8 -*-

import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    import pandas
import numpy

class ItemPipeline(object):

    """ItemPipeline receives items from Spider and converts them to DataFrames.
    """

    df_score = None
    df_tune = None

    data_score = []
    data_tune = []

    current_id = 0

    feed_csv_uri = None

    def __init__(self, feed_csv_uri):

        self.feed_csv_uri = feed_csv_uri

    def process_item(self, item, spider):

        """process_item stores items in arrays `self.data_score` and
        `self.data_tune`.
        """

        if not 'data' in item:
            return item

        item_score = item['data']
        for line in item_score:
            line['tune_id'] = self.current_id
            self.data_score.append(line)
        
        item_tune = item['tune']
        item_tune['id'] = self.current_id
        self.data_tune.append(item_tune)

        self.current_id += 1

        return item
    
    def open_spider(self, spider):

        self.current_id = 0

    def close_spider(self, spider):

        """close_spider converts the arrays into pandas.DataFrames and stores
        them in FEED_CSV_URI as csv files.
        """

        if len(self.data_score) == 0 or len(self.data_tune) == 0:
            return

        self.df_score = pandas.DataFrame(self.data_score)
        self.df_score = self.df_score.astype(
            {
                'rank': numpy.int,
                'score': numpy.int,
                'tune_id': numpy.int,
            }
        )
        self.df_score = self.df_score.set_index(['rank', 'tune_id'])
        self.df_score.to_csv(self.feed_csv_uri + '/scores.csv', encoding='utf-8')

        self.df_tune = pandas.DataFrame(self.data_tune)
        self.df_tune = self.df_tune.astype(
            dtype={
                'id': numpy.int,
                'level': numpy.int,
            }
        )
        self.df_tune = self.df_tune.set_index('id')
        self.df_tune.to_csv(self.feed_csv_uri + '/tunes.csv',  encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            feed_csv_uri=crawler.settings.get('FEED_CSV_URI'),
        )

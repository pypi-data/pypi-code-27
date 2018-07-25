'''Wrapper for Gistapp.com's dataset download endpoint'''

import requests
import csv
import numpy as np
import pandas as pd
import json

# Gist's SSL is less than ideal, so disable the warnings!
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Gisterize:
    '''
    Gisterize

    Attributes:
        feature_names -- numpy array of features in the Gisterize dataset
        data -- 2d numpy array of the Gisterize dataset
    '''

    def __init__(self, data_source_link=False):
        '''
        Gisterize init should be able to run the initialize tasks and get the visualization data formatted and ready to use

        Arguments:
            data_source_link -- the link to a visualizaion on gistapp to grab the source data from
        '''
        if data_source_link:
            self.download_data(data_source_link)

    def download_data(self, data_source_link):
        if not 'gistapp' in data_source_link:
            raise Exception('Please provide a link to a visualization on gistapp.com')
        self.data_source_link = data_source_link
        self.__set_dataset_id_from_viz()
        self.__set_team_subdomain()
        self.__get_raw_data()
        self.__data_in_numpy_array()

    def __set_dataset_id_from_viz(self):
        '''
        Get the dataset id from the given data_source_link
        '''
        r = requests.get(self.data_source_link, verify=False)
        # Make sure that we've requested an actual dataset link
        if not 'datasetId: \'' in r.text:
            raise Exception('Please provide a link to a visualization on gistapp.com')
        # Find the index where the datasetId is passed to options in the script tag
        dataset_id_index = r.text.find('datasetId: \'') + 12
        self.dataset_id = r.text[dataset_id_index:dataset_id_index+24]

    def __set_team_subdomain(self):
        '''
        Set the team subdomain from the data_source_link
            This is really hacky, but it is needed for a correct call to
            /api/dataset/download.
        '''
        index_first_dot = self.data_source_link.find('.')
        self.subdomain = self.data_source_link[8:index_first_dot]

    def __get_raw_data(self):
        '''
        Gets the raw data by making a request to api/dataset/download
        '''
        r = requests.get('https://{}.gistapp.com/api/dataset/download/{}?originalOrModified=modified'.format(self.subdomain, self.dataset_id), verify=False)
        if r.status_code == 403:
            raise Exception('Please use a gistapp visualization that is available to download.')
        self.raw_data = r.text

    def __data_in_numpy_array(self):
        '''
        Puts the raw_data in a numpy array
        '''
        data_file = csv.reader(self.raw_data.splitlines())
        self.feature_names = np.array(next(data_file))
        # Make a list and go through the rest of the data_file and append it to self.data
        self.data = list()
        for row in data_file:
            self.data.append(row)
        self.data = np.array(self.data)

    def __to_dictionary(self):
        '''
        Returns the current object's key attributes as a dictionary
        '''
        return {
            'dataset_id': self.dataset_id,
            'subdomain': self.subdomain,
            'data_source_link': self.data_source_link
        }


    def save_gisterize(self, filename='default'):
        '''
        Saves the current gisteize object to a json file

        Arguments:
            filename -- the filename and path to save the gisterize object to
        '''
        with open('{}.json'.format(filename), 'w+') as out:
            json.dump(self.__to_dictionary(), out)

    def load_gisterize(self, filename='default.json'):
        '''
        Loads the gisterize from a pickle

        Arguments:
            filename -- the filename to load the json from
        '''
        with open('{}'.format(filename), 'r+') as reader:
        # Load the gisterize and assign all the values to self
            loaded_gisterize = json.loads(reader.read())
            self.dataset_id = loaded_gisterize['dataset_id']
            self.subdomain = loaded_gisterize['subdomain']
            self.data_source_link = loaded_gisterize['data_source_link']
        # Now we can redownload the data from the saved json
        self.download_data(self.data_source_link)

    def get_pandas_dataframe(self):
        '''
        Returns a pandas dataframe of the Gisterize
        '''
        return pd.DataFrame(self.data, columns=self.feature_names)
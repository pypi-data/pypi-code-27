import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import time
URL = 'https://www.monster.com/jobs/search'

class MonsterScan:
    '''Monster scan object.
    '''
    def __init__(self, search_query, location=None, pages=1):
        self.search_query = search_query
        self.location = location
        self.pages = pages
        self.params ={  'q': search_query,
                        'where': location,
                        'page': pages}

    def search(self):
        '''Try to get the search page.
        '''
        self.response = requests.get(URL, params = self.params)


    def get_urls(self):
        '''Looking for job Internet link.
        '''
        self.soup = bs(self.response.content, 'lxml')
        self.preliminary_data = self.soup.find('div', class_ = 'mux-search-results')
        self.raw_urls_list = list(filter(lambda x: len(str(x))>500,
            self.preliminary_data.find_all('a', href=True)))
        self.urls_list = [i['href'] for i in self.raw_urls_list]
    

    def parce_urls(self):
        '''Gets a description for each job.
        '''
        self.vacancies_list = list()
        for url in self.urls_list:
            try:
                self.vacancy = requests.get(url)
            except requests.exceptions.ConnectionError:
                continue
            self.soup = bs(self.vacancy.content, 'lxml')
            try:
                self.vacancies_list.append(self.soup.find('div', class_ = 'details-content ').contents[1].get_text())
            except AttributeError:
                pass
         
    def save_vacancies(self, filename='vacancies.csv'):
        '''Saves job description.
        '''
        with open(filename, 'w') as out:
            for vacancy in self.vacancies_list:
                out.write(vacancy+'\n')


if __name__ == '__main__':
    ms = MonsterScan('data science')
    ms.search()
    ms.get_urls()
    ms.parce_urls()
    ms.save_vacancies('data_science.csv')

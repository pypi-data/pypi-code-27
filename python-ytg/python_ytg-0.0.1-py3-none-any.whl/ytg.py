import requests

class Api():
    """
    Connect to YourText.Gugu API to create guides, 
    get keyword recommendations and check your content optimization level.
    """

    def __init__(self, api_key, ytg_url='https://yourtext.guru/api'):
        """
        Get your API key from https://yourtext.guru/profil/api  
        """
        self.api_key = api_key
        self.headers = {'KEY': self.api_key, 'accept': "application/json", 'accept-encoding': "gzip, deflate"}
        self.ytg_url = ytg_url

    def create_guide(self, query, lang='fr_fr', guide_type='premium'):
        """
        Creates a single guide via YourText.Guru API. 
        Returns guide_id, or `None` in case of error.  
        
        Arguments:  
        - query: the search request (please remove special characters & punctuation, or you might encounter bugs)
        - lang: language and Google version. `fr_fr`, `en_us`, `en_gb`, ...   
        - guide_type: `premium` or `oneshot`  
        """
        payload = {'lang': lang, 'type': guide_type, 'query': query}
        url = '{}/guide/'.format(self.ytg_url)
        r = requests.post(url, data=payload, headers=self.headers)
        if r.status_code == 200:
            return r.json().get('guide_id')
        return None

    def get_guide(self, guide_id):
        """
        Retrives YTG guide from API.  
        Returns raw JSON guide, or `None` in case of error.  

        Arguments:  
        - guide_id: the ID of the guide to retrieve  
        """
        url = '{}/guide/{}'.format(self.ytg_url,guide_id)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()[0]
        return None

    def get_scores(self, guide_id, content):
        """
        Tests a piece of content against a YTG guide and returns optimization and danger scores.  

        Arguments:  
        - guide_id: the ID of the guide to compare your content to
        - content: the content you want to check
        """
        payload = {'content': content}
        r = requests.post('{}/check/{}'.format(self.ytg_url, guide_id),
                    data=payload, headers=self.headers)

        if r.status_code == 200:
            results = dict()
            results['score'] = r.json().get('score')
            results['danger'] = r.json().get('danger')
            return results
        return None

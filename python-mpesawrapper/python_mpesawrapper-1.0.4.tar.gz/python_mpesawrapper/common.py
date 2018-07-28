import json
import requests as link
from requests.auth import HTTPBasicAuth
from decouple import config
class RequestHandler:
	def __init__(self):
		self.debug = False
		self.base_url = 'https://api.safaricom.co.ke/' if self.debug is False else 'https://api.safaricom.co.ke/'

	def makeRequest(self,**kwargs):
		try:
			data=kwargs.pop('data')
			print(data)
			token=json.loads(link.get(self.base_url+'oauth/v1/generate?grant_type=client_credentials',auth=HTTPBasicAuth(config('consumer_key'),config('consumer_secret'))).text)['access_token']
			headers={}
			headers['Content-Type']='application/json'
			headers['Authorization']='Bearer'+' '+token
			response=lambda headers:link.post(self.base_url+kwargs.pop('url'),json=data,headers=headers).text
			return response(headers)
		except Exception as e:
			raise  e
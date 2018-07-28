import time,datetime,base64
from decouple import config

from python_mpesawrapper.common import  RequestHandler


class MpesaExpressHandler:
	@staticmethod
	def handle(**kwargs):
		try:
			mobile_number=kwargs.pop('mobile_number')
			timestamp=datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
			concatinatedString= config('MEShortcode')+config('MEpasskey')+str(timestamp)
			requestbody={}
			requestbody['BusinessShortCode']=config('MEShortcode')
			requestbody['Password']=base64.b64encode(concatinatedString.encode('utf-8')).decode('utf=8')
			requestbody['Timestamp']=timestamp
			requestbody['TransactionType']='CustomerPayBillOnline'
			requestbody['Amount']=kwargs.pop('amount')
			requestbody['PartyA']=mobile_number
			requestbody['PartyB']=config('MEShortcode')
			requestbody['PhoneNumber']=mobile_number
			requestbody['CallBackURL']=config('MECallBackURL')
			requestbody['AccountReference']=str('{:%y%m%d%H%M%S}'.format(datetime.datetime.now()))
			requestbody['TransactionDesc']='Lipa na Mpesa STK'
			return RequestHandler().makeRequest(
				url='mpesa/stkpush/v1/processrequest',
				data=requestbody
			)
		except Exception as e:
			raise  e
class MpesaExpressQueryHandler:
	@staticmethod
	def handle(**kwargs):
		try:
			timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
			concatinatedString = config('MEShortcode') + config('MEpasskey') + str(timestamp)
			requestbody={}
			requestbody['BusinessShortCode']=config('MEShortcode')
			requestbody['Password']=base64.b64encode(concatinatedString.encode('utf-8')).decode('utf=8')
			requestbody['Timestamp']=str(timestamp)
			requestbody['CheckoutRequestID']=kwargs.pop('CheckoutRequestID')
			return RequestHandler().makeRequest(
				url='mpesa/stkpushquery/v1/query',
				data=requestbody
			)
		except Exception:
			raise Exception



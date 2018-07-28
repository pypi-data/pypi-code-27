import base64,datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from decouple import config
from python_mpesawrapper.common import  RequestHandler
class B2CHandler:
	@staticmethod
	def handle(**kwargs):
		try:
			amount=kwargs.pop('amount')
			mobile_number=kwargs.pop('mobile_number')
			requestbody={}
			#create json
			requestbody['InitiatorName']=config('b2cInitiatorName')
			requestbody['SecurityCredential']=base64.b64encode(PKCS1_v1_5.new(RSA.importKey(open('pubkey.pem').read())).encrypt(config('init_password').encode("utf-8")))
			requestbody['CommandID']='BusinessPayment'
			requestbody['Amount']=amount
			requestbody['PartyA']=config('b2cShortcode')
			requestbody['PartyB']=mobile_number
			requestbody['Remarks']='B2c Payment'
			requestbody['QueueTimeOutURL']=config('b2cTimeoutUrl')
			requestbody['ResultURL']=config('b2cResultUrl')
			requestbody['Occassion']=str(datetime.datetime.now())
			return RequestHandler().makeRequest(
				url='mpesa/b2c/v1/paymentrequest',
				data=requestbody
			)
		except Exception as e:
			raise  e
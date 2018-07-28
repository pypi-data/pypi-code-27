import base64,datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from decouple import config
from python_mpesawrapper.common import  RequestHandler
class B2bHandler:

	@staticmethod
	def handle(**kwargs):
		try:
			requestbody={}
			requestbody['Initiator']=config('b2bInitiator')
			requestbody['SecurityCredential']=base64.b64encode(PKCS1_v1_5.new(RSA.importKey(open('pubkey.pem').read())).encrypt(config('init_password').encode("utf-8"))).decode('utf-8')
			requestbody['CommandID']=kwargs.pop('command')
			requestbody['SenderIdentifierType']=kwargs.pop('senderType')
			requestbody['RecieverIdentifierType']=kwargs.pop('recieverType')
			requestbody['Amount']=int(kwargs.pop('amount'))
			requestbody['PartyA']=config('b2bShortcode')
			requestbody['PartyB']=kwargs.pop('recipient')
			requestbody['AccountReference']=str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
			requestbody['Remarks']='B2B Payment'
			requestbody['QueueTimeOutURL']=config('b2bTimeoutURL')
			requestbody['ResultURL']=config('b2bResultURL')
			return RequestHandler().makeRequest(
				url='mpesa/b2b/v1/paymentrequest',
				data=requestbody
			)
		except Exception as e:
			raise  e

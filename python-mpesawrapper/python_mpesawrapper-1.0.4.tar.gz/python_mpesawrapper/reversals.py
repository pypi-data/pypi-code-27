from  decouple import  config
import base64,datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from decouple import config
from python_mpesawrapper.common import  RequestHandler
class reversalHandler:
	@staticmethod
	def handle(**kwargs):
		try:
			requestbody={}
			requestbody['Initiator']=config('reversalInitiator')
			requestbody['SecurityCredential']=base64.b64encode(PKCS1_v1_5.new(RSA.importKey(open('pubkey.pem').read())).encrypt(config('reversalinit_password').encode("utf-8"))).decode('utf-8')
			requestbody['CommandID']='TransactionReversal'
			requestbody['TransactionID']=kwargs.pop('mpesaTransactionID')
			requestbody['Amount']=kwargs.pop('amount')
			requestbody['ReceiverParty']=config('reverseShortcode')
			requestbody['RecieverIdentifierType']=11
			requestbody['ResultURL']=config('reversResultURL')
			requestbody['QueueTimeOutURL']=config('reverseQueueTimeOutURL')
			requestbody['Remarks']=kwargs.pop('remarks')
			requestbody['Occasion']=str('{:%y%m%d%H%M%S}'.format(datetime.datetime.now()))
			return RequestHandler().makeRequest(
				url='mpesa/reversal/v1/request',
				data=requestbody
			)
		except Exception as e:
			raise e



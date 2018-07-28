from  decouple import  config
import base64,datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from decouple import config
from python_mpesawrapper.common import  RequestHandler
class statusQueryHandler:
	@staticmethod
	def handle(**kwargs):
		try:
			requestbody={}
			requestbody['Initiator']=config('sqInitiator')
			requestbody['SecurityCredential']=base64.b64encode(PKCS1_v1_5.new(RSA.importKey(open('pubkey.pem').read())).encrypt(config('init_password').encode("utf-8")))
			requestbody['CommandID']='TransactionStatusQuery'
			requestbody['TransactionID']=kwargs.pop('mpesaTransactionID')
			requestbody['PartyA']=config('sqShortcode')
			requestbody['IdentifierType']=kwargs.pop('initiator')
			requestbody['ResultURL']=config('sqResultURL')
			requestbody['QueueTimeOutURL']=config('sqQueueTimeOutURL')
			requestbody['Remarks']='Status query'
			requestbody['Occasion']=str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
			return RequestHandler().makeRequest(
				url='transactionstatus/v1/query',
				data=requestbody
			)
		except Exception as e:
			raise e


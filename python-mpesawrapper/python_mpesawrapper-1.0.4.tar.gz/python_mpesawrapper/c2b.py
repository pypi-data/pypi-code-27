from python_mpesawrapper.common import RequestHandler


class c2bHandler:
	@staticmethod
	def handler(**kwargs):
		try:
			requestbody={}
			requestbody['ShortCode']=kwargs.pop('ShortCode')
			requestbody['ResponseType']='Completed'
			requestbody['ConfirmationURL']=kwargs.pop('ConfirmationURL')
			requestbody['ValidationURL']=kwargs.pop('ValidationURL')
			return RequestHandler().makeRequest(
				url='mpesa/c2b/v1/registerurl',
				data=requestbody
			)
		except Exception:
			raise  Exception
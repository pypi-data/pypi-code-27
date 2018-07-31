import logging
import traceback
from functools import wraps
import sys
from fc.cloudtrailsdk.model.event import Event
from fc.cloudtrailsdk.utils.functions import send_custom_logger, send_exception_logger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_apigateway_response(response):
    return {
        'statusCode': response['code'],
        'body': json.dumps(response)
    }

def cloudtrails_apigatweay(app_name="undefined", app_version="undefined"):
	def cloudtrails_apigatweay_tracker_decorator(func):
        @wraps(func)
        def apigatweay_wrapper(event, context):

        	# Intentar obtener el resultado de la funcion original
        	try:
				result = func(event, context)
			except Exception as ex:
				# Si la funcion original dio error logear un evento exception y retornar un 500 generico
				try:
                    send_exception_logger(app_name, app_version)
                    logger.error(e.message)
                except Exception as e:
                    logger.error(e.message) 
				error_response = {'message': 'Ha ocurrido un error no controlado', 'code': 500}
		        result = build_apigateway_response(error_response)

		    # Construir el evento cloudtrails y logearlo

		    #Extraer los datos del evento Apigateway Proxy Integration
		    func_name = func.__name__
		    request_data = {
		    	"EventType": "WebApiCall",
		    	'Method': func_name,
		        "RequestMethod": event['httpMethod'],
		        "RequestScheme": "https",
		        "RequestHost": event['headers'].get('Host', ''),
		        "RequestPath": event.get('path', ''),
		        "RequestQueryString": json.dumps(event.get('queryStringParameters', {})),
		        "ClientIP": event['headers'].get('X-Forwarded-For', ''),
		        "UserAgent": event['headers'].get('User-Agent', ''),
		        "RequestPayload": json.dumps(event.get('body', {})),
		        "ResponsePayload": json.dumps(result.get('body', {})),
		        "ResponseHttpStatus": result.get('statusCode', '0'),
		        "Headers": json.dumps(event.get('headers', {}))
		    }

		    #Poner Custom Dimensions si hay alguna
	    	if result.get('cloudtrails_dimensions', None) is not None:
	            request_data['Dimensions'].= result.get('cloudtrails_dimensions', None)
	            result.pop('cloudtrails_dimensions', None)

		    #Poner Custom  properties si hay alguna
		    if result.get('cloudtrails_properties', None) is not None:
	            request_data.update(result.get('cloudtrails_properties', None))
	            result.pop('cloudtrails_properties', None)


		    send_custom_logger(app_name=app_name, app_version=app_version, request_data)


			# Retornar el resultado final
			return result
		
		return apigatweay_wrapper

    return cloudtrails_apigatweay_tracker_decorator
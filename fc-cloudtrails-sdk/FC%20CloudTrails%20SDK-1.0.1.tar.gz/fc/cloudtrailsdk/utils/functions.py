import json
import os
import logging
import sys
import traceback

from fc.cloudtrailsdk.client.tracker import Tracker
from fc.cloudtrailsdk.model.event import Event, ExceptionEvent, DependencyEvent

logger = logging.getLogger(__name__)


def configure_tracker(app_name="", app_version="", tracker_environment=None):
    region = os.environ.get("AWS_REGION")
    tracker_environment = os.environ.get("TRACKER_ENVIRONMENT",
                                         "eCloudTrailsStreamQA") if tracker_environment is None else tracker_environment
    tracker = Tracker(
        tracker_environment,
        region=region,
        app_name=app_name,
        app_version=app_version
    )
    return tracker


def send_custom_logger(app_name="", app_version="", tracker_environment=None, **properties):
    try:
        tracker = configure_tracker(app_name=app_name, app_version=app_version,
                                    tracker_environment=tracker_environment)
        custom_event = Event()

        # Determinar si las propiedades contienen dimensiones y en tal caso actualizarlos
        if properties.get('Dimensions', None) is not None:
            custom_event.Dimensions.update(properties.get('Dimensions', None))
            properties.pop('Dimensions', None)

        # Determinar si las propiedades contienen un EventType
        if properties.get('EventType', None) is not None:
            custom_event.EventType = properties.get('EventType', None)
            properties.pop('EventType', None)

        custom_event.Properties.update(properties)
        tracker.track_event(custom_event)
    except Exception as e:
        logger.error(e.message)


def send_exception_logger(app_name="", app_version="", tracker_environment=None, **properties):
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tracker = configure_tracker(app_name=app_name, app_version=app_version,
                                    tracker_environment=tracker_environment)
        exception_event = ExceptionEvent(exc_value.__str__(), exc_type.__name__, traceback.format_exc(), **properties)

        # Determinar si las propiedades contienen dimensiones y en tal caso actualizarlos
        if properties.get('Dimensions', None) is not None:
            exception_event.Dimensions.update(properties.get('Dimensions', None))
            exception_event.Properties('Dimensions', None)

        tracker.track_exception(exception_event)
    except Exception as e:
        logger.error(e.message)


def send_dependency_logger(dependency_name, dependency_duration):
    try:
        tracker = configure_tracker()
        dependency_event = DependencyEvent(dependency_name, dependency_duration)
        tracker.track_dependency(dependency_event)
    except Exception as e:
        logger.error(e.message)


def send_cloudtrails_apigateway_event(app_name, app_version, event, response, **properties):
    """
    Permite enviar a cloutrails los request
    :param request:
    :param response:
    :return:
    """
    #Extraer los datos del evento Apigateway Proxy Integration
    request_data = {
        "RequestMethod": event['httpMethod'],
        "RequestScheme": "https",
        "RequestHost": event['headers'].get('Host', ''),
        "RequestPath": event.get('path', ''),
        "RequestQueryString": json.dumps(event.get('queryStringParameters', {})),
        "ClientIP": event['headers'].get('X-Forwarded-For', ''),
        "UserAgent": event['headers'].get('User-Agent', ''),
        "RequestPayload": json.dumps(event.get('body', {})),
        "ResponsePayload": json.dumps(response),
        "ResponseHttpStatus": response.get('code', '0'),
        "Headers": json.dumps(event.get('headers', {}))
    }
    properties.update(request_data)

    send_custom_logger(app_name=app_name, app_version=app_version, **properties)

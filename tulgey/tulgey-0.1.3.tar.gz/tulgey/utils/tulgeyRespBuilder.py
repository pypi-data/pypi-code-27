from typing import Mapping, Any, Tuple, Optional, Union
import json

headers = {'Content-Type': 'application/json; charset=utf-8'}

def buildBadRequestResponse(message: Optional[str]) -> Tuple[str, int,  Mapping[str, str]]:
    return (
        json.dumps({"status": False, "reason": "Bad Request", "message": message}),
        400,
        headers
    )


def buildValidResponse(jsonDict: Union[str, Mapping[str, Any]]) -> Tuple[str, int, Mapping[str, str]]:
    return json.dumps({"status": True, "data": jsonDict}, indent=4), 200, headers


def buildNotFoundResponse(message: Optional[str]) -> Tuple[str, int, Mapping[str, str]]:
    return json.dumps({"status": False, "reason": "Not Found", "message": message}), 200, headers

def buildErrorResponse(jsonDict: Union[str, Mapping[str, Any]]) -> Tuple[str, int, Mapping[str, str]]:
    return json.dumps({"status": False, "reason": "Error", "message": jsonDict}), 500, headers
import base64
import datetime
import hashlib
import hmac

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


class Auth:
    def __init__(self, secretId: str, secretKey: str, headers: dict = None):
        self.secretKey = secretKey
        self.secretId = secretId
        self.headers = headers if headers else {}

    def generateHeaders(self) -> dict:
        self.headers['Date'] = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        authStr = f'hmac id="{self.secretId}", algorithm="hmac-sha1", headers="{" ".join(key.lower() for key in self.headers.keys())}", signature='
        signStr = '\n'.join(
            f'{key.lower()}: {value}' for key, value in self.headers.items())
        originSign = hmac.new(self.secretKey.encode(), signStr.encode(),
                              hashlib.sha1).digest()
        b64Sign = base64.b64encode(originSign).decode()
        authorization = authStr + f'"{b64Sign}"'
        self.headers['Authorization'] = authorization
        return self.headers

import sys
import typing
import logging
import traceback

from apistar import App, http
from flask.sessions import SecureCookieSessionInterface

from .components import DummyFlaskApp
from .session import Session


class SessionHook(object):

    def __init__(self):
        self.session_interface = SecureCookieSessionInterface()

    def on_response(self,
                    app: DummyFlaskApp,
                    resp: http.Response,
                    session: Session):
        self.session_interface.save_session(app, session, resp)


class ErrorHook(object):
    """
    处理异常
    """
    errors = {999: "Unknown error"}

    def on_error(self, error: Exception, app:App) -> http.Response:
        """
        Handle error
        """
        code = 999
        message = None
        if not isinstance(error.args[0], (tuple, list)) \
                or len(error.args[0]) < 2:
            if isinstance(error.args[0], int):
                code = error.args[0]
            else:
                message = error.args[0]
        else:
            code, message = error.args[0][:2]

        code = int(code)
        # apistar不支持在on_request时打断后续执行直接返回response
        # 所以在只能通过raise异常来通过异常参数传递响应。
        if isinstance(message, http.Response):
            return message

        if message is None:
            message = self.errors.get(code, "Not configured error")

        payload = {
            "code": code,
            "value": None,
            "errcode": code,
            "message": message,
        }
        if app.debug:
            payload["detail"] = "".join(traceback.format_exc())
        traceback.print_exc()
        return http.JSONResponse(payload)

    @classmethod
    def register(cls,
                 errors: typing.Union[typing.List[typing.Tuple[int, str]],
                                      typing.Mapping[int, str]]):
        cls.errors.update(errors)


class AccessLogHook(object):
    fmt = '{host} - - [{asctime}] {method} {path} {protocol}' \
          ' {status} {content_length} {agent}'

    def __init__(self):
        self.logger = logging.getLogger("access")
        self.logger.propagate = False
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(10)
        handler.setFormatter(logging.Formatter(self.fmt, style="{"))
        self.logger.addHandler(handler)

    def on_response(self,
                    host: http.Host,
                    path: http.Path,
                    protocol: http.Scheme,
                    method: http.Method,
                    resp: http.Response,
                    user_agent: http.Header):
        self.log(host, path, protocol, method, resp.status_code,
                 resp.headers["Content-Length"], user_agent)

    def on_error(self,
                 host: http.Host,
                 path: http.Path,
                 protocol: http.Scheme,
                 method: http.Method,
                 resp: http.Response,
                 user_agent: http.Header) -> http.Response:
        self.log(host, path, protocol, method, resp.status_code,
                 resp.headers["Content-Length"], user_agent)
        return resp

    def log(self, host, path, protocol, method, status, content_length, agent):
        self.logger.info("", extra={"host": host,
                                    "path": path,
                                    "protocol": protocol,
                                    "method": method,
                                    "status": status,
                                    "content_length": content_length,
                                    "agent": agent})

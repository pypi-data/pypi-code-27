import logging

from apistar import ASyncApp, App, exceptions
from apistar.http import Response, JSONResponse
from apistar.server.components import ReturnValue

from .bases.service import Service
from .bases.hooks import ErrorHook, AccessLogHook, SessionHook
from .bases.components import SettingsComponent
from .helper import load_packages, routing, print_routing, TypeEncoder, \
    bug_fix, find_children, enhance_response

# 修复uvicorn bug
bug_fix()

__all__ = ["Application"]

logger = logging.getLogger("star_builder.app")
enhance_response(Response)
JSONResponse.options["default"] = TypeEncoder().default


class FixedAsyncApp(ASyncApp):

    def exception_handler(self, exc: Exception) -> Response:
        if isinstance(exc, exceptions.HTTPException):
            return JSONResponse(exc.detail, exc.status_code, exc.get_headers())
        raise exc

    def error_handler(self, return_value: ReturnValue) -> Response:
        if isinstance(return_value, Response):
            return return_value
        return super().error_handler()


class FixedApp(App):

    def exception_handler(self, exc: Exception) -> Response:
        if isinstance(exc, exceptions.HTTPException):
            return JSONResponse(exc.detail, exc.status_code, exc.get_headers())
        raise exc

    def error_handler(self, return_value: ReturnValue) -> Response:
        if isinstance(return_value, Response):
            return return_value
        return super().error_handler()


def application(template_dir=None,
                static_dir=None,
                packages=None,
                schema_url='/schema/',
                docs_url='/docs/',
                static_url='/static/',
                event_hooks=None,
                settings_path="settings",
                debug=True,
                async=True):
    """
       参数指定选择使用异步app还是同步app
       可以动态发现当前项目根目录下所有routes的service中的handler
    """
    load_packages(".")
    include = routing(Service, None)
    SettingsComponent.register_path(settings_path)

    if include:
        routes = [include]
        print_routing(routes, callback=logger.debug)
    else:
        logger.info("Noting to route. ")
        routes = []
    hooks = [AccessLogHook(), SessionHook(), ErrorHook()] + (event_hooks or [])
    app = (FixedAsyncApp if async else FixedApp)(
        routes,
        template_dir=template_dir,
        static_dir=static_dir,
        packages=packages,
        schema_url=schema_url,
        docs_url=docs_url,
        static_url=static_url,
        components=find_children(),
        event_hooks=hooks)

    app.debug = debug
    return app


Application = application

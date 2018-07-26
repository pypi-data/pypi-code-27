"""Checks request for CSRF token.
If CSRF is absent or invalid:
    If it's a get request - installs new token in cookie and redirects to same page.
    In other cases - raises 403 exception (forbidden).

Requires some session middleware to be installed.
That session plugin must use such interface:
    request['session'].get('variable') or request['session']['variable']
    request['session']['variable'] = 4
For example, 'sanic_session' (https://github.com/subyraman/sanic_session) will fit.
"""

import uuid
import sanic.response
from sanic.exceptions import Forbidden


def install_middleware(app):
    """Installs middleware, that protects session with CSRF token
    to Sanic 'Application' class instance.
    'app' - instance of 'Application' class, that will be protected.
    """
    @app.middleware('request')
    async def sanic_csrf_request(request):
        if not request['session'].get('csrf_token') or not request.cookies.get('csrf_token'):
            if request.method == 'GET':
                response = sanic.response.redirect(request.path)
                install_csrf_token(request['session'], response)
                return response
            else:
                raise Forbidden('Wrong CSRF token')
        else:
            if request.cookies.get('csrf_token') == request['session'].get('csrf_token'):
                pass
            else:
                raise Forbidden('Wrong CSRF token')


def install_csrf_token(session, response):
    """Installs new random csrf token to session and responce.cookies object.
    """
    csrf_token = str(uuid.uuid4())
    session['csrf_token'] = csrf_token
    response.cookies['csrf_token'] = csrf_token
    response.cookies['csrf_token']['max-age'] = 600
    response.cookies['csrf_token']['samesite'] = 'strict'

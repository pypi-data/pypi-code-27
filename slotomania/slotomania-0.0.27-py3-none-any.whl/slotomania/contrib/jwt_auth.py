import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

from slotomania.exceptions import NotAuthenticated

User = get_user_model()


def authenticate_request(request):
    header = request.META.get("HTTP_AUTHORIZATION")
    prefix, token = header.split()
    if not token:
        raise NotAuthenticated()

    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature as e:
        raise NotAuthenticated(str(e))
    except jwt.DecodeError as e:
        raise NotAuthenticated(str(e))
    except jwt.InvalidTokenError as e:
        raise NotAuthenticated(str(e))

    user = authenticate_credentials(payload)
    request.user = user


def authenticate_credentials(payload):
    username = payload.get("username")

    if not username:
        raise NotAuthenticated("Invalid payload")

    try:
        user = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        raise NotAuthenticated("Invalid signature")

    if not user.is_active:
        raise NotAuthenticated("User account is disabled")

    return user


def jwt_decode_handler(token):
    options = {
        'verify_exp': True,
    }
    secret_key = settings.SECRET_KEY
    return jwt.decode(
        token,
        secret_key,
        True,
        options=options,
        leeway=0,
        audience=None,
        issuer=None,
        algorithms=['HS256']
    )

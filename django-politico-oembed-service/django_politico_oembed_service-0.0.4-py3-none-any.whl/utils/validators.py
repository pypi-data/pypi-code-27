from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def check_domain(url, domain):
    """
    Checks if URL is valid and is from domain, e.g., twitter.com.
    """
    validate = URLValidator()
    try:
        validate(url)
        return domain in url
    except ValidationError:
        return False

from django.conf import settings
from requests_oauthlib import OAuth1

import requests


def get_display_name(user_id, oauth_token, oauth_token_secret):
    oauth = OAuth1(
        settings.SOCIAL_AUTH_TWITTER_KEY,
        settings.SOCIAL_AUTH_TWITTER_SECRET,
        oauth_token,
        oauth_token_secret
    )

    response = requests.get(
        'https://api.twitter.com/1.1/users/show.json?user_id={}'.format(user_id),
        auth=oauth
    ).json()

    return response['name']

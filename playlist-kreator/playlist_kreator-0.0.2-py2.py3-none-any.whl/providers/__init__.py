from playlist_kreator.providers import gmusic, spotify

PROVIDERS = {
    'gmusic': gmusic,
    'spotify': spotify,
}


def get_provider(provider_name):
    return PROVIDERS[provider_name]

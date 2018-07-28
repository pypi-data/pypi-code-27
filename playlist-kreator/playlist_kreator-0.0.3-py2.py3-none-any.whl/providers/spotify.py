import webbrowser

import spotipy
from furl import furl

# This is the playlist-kreator app client id, we don't need the secret, as we do client side auth
SPOTIFY_CLIENT_ID = 'b1c5cfc647d146e0955db636cf387132'


def create_playlist(playlist_name, artists, user_info, max_top_tracks=2):
    sp = spotipy.Spotify(auth=user_info['token'])

    username = user_info['username']
    playlist = sp.user_playlist_create(username, playlist_name)
    song_ids = []

    print()

    for artist in artists:
        result = sp.search(artist, limit=1, type='artist')
        if len(result['artists']['items']) == 0:
            print('{}: Does not exist in Spotify. Skipping'.format(artist))
            continue

        print('Found {}'.format(artist))

        artist_id = result['artists']['items'][0]['id']

        top_tracks = sp.artist_top_tracks(artist_id)
        for track in top_tracks['tracks'][:max_top_tracks]:
            song_ids.append(track['id'])

    max_tracks_per_request = 100
    i = 0
    nb_tracks = len(song_ids)
    while i*max_tracks_per_request < nb_tracks:
        subsong_ids = song_ids[i*max_tracks_per_request:i*max_tracks_per_request+max_tracks_per_request]
        sp.user_playlist_add_tracks(username, playlist['id'], subsong_ids)
        i += 1


def get_user_info(args):
    username = args.username
    if username:
        print("Username: {}".format(username))
    else:
        print("You will need your spotify username. You can get it from: https://www.spotify.com/us/account/overview/")
        username = input("Username: ")

    auth_url = _get_auth_url()
    webbrowser.open(auth_url)

    print('''
        User authentication requires interaction with your
        web browser.
        This will open a page in your browser.
        Paste that url you were directed to to
        complete the authorization.
    ''')

    redirect_url = input('Enter the URL you were redirected to: ')
    # Why #??
    redirect_furl = furl(redirect_url.replace('callback/#access_token', 'callback/?access_token'))
    token = redirect_furl.args['access_token']

    return {
        'token': token,
        'username': username,
    }


def _get_auth_url():
    api_furl = furl('https://accounts.spotify.com/authorize')
    api_furl.args['client_id'] = SPOTIFY_CLIENT_ID
    api_furl.args['redirect_uri'] = 'http://example.com/callback/'
    api_furl.args['scope'] = 'playlist-modify-public'
    api_furl.args['response_type'] = 'token'

    return api_furl.url

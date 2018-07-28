from getpass import getpass
from gmusicapi import Mobileclient


def create_playlist(playlist_name, artists, user_info, max_top_tracks=2):
    email = user_info['username']
    password = user_info['password']

    api = Mobileclient()
    logged_in = api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)

    if not logged_in:
        raise Exception('Could not connect')

    song_ids = []

    for artist_name in artists:
        search = api.search(artist_name)

        if len(search["artist_hits"]) == 0:
            print('{}: Does not exist in Google Music. Skipping'.format(artist_name))
        else:
            artist_id = search["artist_hits"][0]["artist"]["artistId"]
            artist = api.get_artist_info(artist_id, include_albums=False,
                                         max_top_tracks=max_top_tracks, max_rel_artist=0)

            if 'topTracks' not in artist:
                print('{}: Exists but no songs found on Google Music. Skipping'.format(artist_name))
            else:
                song_ids = song_ids + [track['nid'] for track in artist['topTracks']]
                print('{}: Found {} song(s). Will add'.format(artist_name, len(artist['topTracks'])))

    playlist_id = api.create_playlist(playlist_name)
    print('\nCreated playlist "{}" ({})'.format(playlist_name, playlist_id))

    api.add_songs_to_playlist(playlist_id, song_ids)
    print('Added {} songs to the playlist'.format(len(song_ids)))
    print('All done. Enjoy! 🤘')


def get_user_info(args):
    print("It will need an email and an application password for Google Music")
    print("You can set it up here: https://myaccount.google.com/apppasswords\n")

    email = args.username
    if email:
        print("Email: {}".format(email))
    else:
        email = input("Email:")

    password = getpass("Password:")
    print()

    return {
        'email': email,
        'password': password,
    }

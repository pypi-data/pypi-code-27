import argparse
import sys

from playlist_kreator import providers
from playlist_kreator import VERSION
from playlist_kreator.common import read_artists


def main(arguments):
    parser = argparse.ArgumentParser(
        prog='playlist-kreator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            'Create easily playlists.\n'
            '\n'
            'Version: {}\n'
        ).format(VERSION),
    )
    subparsers = parser.add_subparsers(dest='command')

    artists_parser = subparsers.add_parser(
        'artists',
        help="Create a playlist based on a list of artists, using their top songs",
    )
    artists_parser.add_argument('artists_file', help='file with list of artists')
    artists_parser.add_argument('playlist_name', help='name of the playlist')
    artists_parser.add_argument(
        '--provider',
        default='gmusic',
        type=str,
        help='Music Provider. Supported: gmusic, spotify',
    )
    artists_parser.add_argument(
        '--max-songs-per-artist',
        default=2,
        type=int,
        help='max number of songs per artist',
    )
    artists_parser.add_argument(
        '--username',
        help='optional username/email, if not set you will be asked in the prompt',
    )

    subparsers.add_parser('version', help="Print playlist-kreator Version")

    args = parser.parse_args(arguments)

    if args.command == 'version':
        print(VERSION)
    elif args.command == 'artists':
        artists_command(args)
    else:
        parser.print_help()


def artists_command(args):
    artists = read_artists(args.artists_file)
    print("Artists to look for: {}\n".format(artists))

    music_provider = providers.get_provider(args.provider)

    user_info = music_provider.get_user_info(args)
    music_provider.create_playlist(
        args.playlist_name,
        artists,
        user_info,
        max_top_tracks=args.max_songs_per_artist,
    )


if __name__ == '__main__':
    main(sys.argv[1:])

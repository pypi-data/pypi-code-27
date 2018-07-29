import os
import shlex
import subprocess
import musicbrainzngs as musicbrainz
import logging
import re
import shutil


LOGGER = logging.getLogger('impd')
musicbrainz.set_useragent('impd', '0.1.3', 'https://gitlab.com/sj1k/impd')


def find_artwork(name, album, artist, path, music_folder, extract_order,
                 online=True, filepath=None, scraper_regex=None):
    if not os.path.exists(path):
        os.makedirs(path)
    song_location = '{}/{}'.format(music_folder, filepath)
    if not os.path.exists(song_location):
        return None
    cover_path = '{}/{}/{}/cover'.format(path, artist, album)
    if os.path.exists(cover_path):
        logging.debug('Cover: -> {}.'.format(cover_path))
        return cover_path
    folder = os.path.dirname(cover_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    for scraper in extract_order.split(','):
        call = extracters.get(scraper, None)
        if call is not None:
            found = call(name, album, artist, song_location, cover_path,
                         online=online, scraper_regex=scraper_regex)
            if found:
                return cover_path
    return None


def folder_extract(name, album, artist, song_location, cover_path,
                   online=True, scraper_regex=None):
    folder = os.path.dirname(song_location)
    files = os.listdir(folder)
    regex = re.compile(scraper_regex)
    for file in files:
        match = re.match(regex, file)
        if match:
            LOGGER.debug('folder: {}/{} -> {}'.format(
                          folder, file, cover_path))
            os.link('{}/{}'.format(folder, file), cover_path)
            return True
    return False


def ffmpeg_extract(name, album, artist, song_location, cover_path,
                   online=True, scraper_regex=None):
    fullpath = os.path.expanduser('~/.impd/temp.png')
    command = ('ffmpeg -loglevel 0 -y -i "{}" '
               '"{}"'.format(song_location, fullpath))
    command = shlex.split(command)
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return False
    LOGGER.debug('ffmpeg: {}'.format(cover_path))
    shutil.move(fullpath, cover_path)
    return True


def musicbrainz_extract(name, album, artist, song_location, cover_path,
                        online=True, scraper_regex=None):
    if not online:
        return False
    cover = _musicbrainz_cover(name, album, artist)
    if cover is not None:
        _save_artwork(cover, cover_path)
        LOGGER.debug('musicbrainz: {}'.format(cover_path))
        return True
    return False


extracters = {
    'folder': folder_extract,
    'ffmpeg': ffmpeg_extract,
    'musicbrainz': musicbrainz_extract,
}


def _save_artwork(cover_data, cover_path):
    if cover_data is None:
        return None
    dirpath = os.path.dirname(cover_path)
    try:
        os.makedirs(dirpath)
    except FileExistsError:
        pass
    with open(cover_path, 'bw') as f:
        f.write(cover_data)
    return cover_path


def _musicbrainz_cover(title, album, artist):
    recordings = musicbrainz.search_recordings(
            query=title,
            artist=artist).get('recording-list', [])
    if recordings == []:
        return None
    try:
        release_id = recordings[0]['release-list'][0]['id']
        cover = musicbrainz.get_image(release_id, 'front')
    except (KeyError, musicbrainz.WebServiceError):
        return None
    return cover

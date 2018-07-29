import time
import itertools
import logging
import os

import gi

from impd import timing, cover, client, threads

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GObject, Gdk


LOGGER = logging.getLogger('impd')
GObject.threads_init()


class LabelWrap(Gtk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_line_wrap(True)
        self.set_halign(Gtk.Align.START)
        self.set_xalign(0)


class PlaylistItem(Gtk.EventBox):

    cover_loaded = False
    pix = None
    active = False

    def __init__(self, name, artist=None, album=None, duration=None,
                 file_=None, artwork_folder=None, icon_width=35,
                 icon_missing_width=20, songid=None,
                 music_folder=None, scrapers=None, scraper_regex=None):
        super().__init__()
        self.name = name
        self.artist = artist
        self.album = album
        self.file_ = file_
        self.duration = duration
        self.art_folder = os.path.expanduser(artwork_folder)
        self.music_folder = os.path.expanduser(music_folder)
        self.icon_width = icon_width
        self.icon_missing_width = icon_missing_width
        self.songid = songid
        self.scrapers = scrapers
        self.scraper_regex = scraper_regex
        self.create_widgets()
        self.show_all()
        # self.connect('draw', self.draw)
        self.connect('realize', self.realize)
        self.connect('enter-notify-event', self.mouse_in)
        self.connect('leave-notify-event', self.mouse_out)

    def realize(self, *_):
        self.window = self.get_window()
        return None

    def mouse_in(self, *_):
        cursor = Gdk.Cursor.new(Gdk.CursorType.HAND1)
        self.window.set_cursor(cursor)
        if not self.active:
            self.set_highlight(True)
        return None

    def mouse_out(self, *_):
        if not self.active:
            self.set_highlight(False)
        return None

    def draw(self, *_):
        self._draw()
        return None

    def _draw(self, artwork_cache={}, online=True):
        LOGGER.debug('Cover: {}'.format(self.file_))
        if self.cover_loaded:
            return False, None, None
        artwork = cover.find_artwork(self.name, self.album, self.artist,
                                     self.art_folder, self.music_folder,
                                     self.scrapers,
                                     filepath=self.file_, online=online,
                                     scraper_regex=self.scraper_regex)
        if artwork is not None:
            from_cache = artwork in artwork_cache
            self.cover_loaded = True
            if from_cache:
                self.pix = artwork_cache[artwork]
            else:
                self.pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    artwork,
                    self.icon_width, -1,
                    preserve_aspect_ratio=True)
            self.set_artwork(self.pix)
            self.set_padding(10)
            return from_cache, self.pix, artwork
        else:
            self.cover_loaded = False
            self.w_line.set_child_packing(
                self.w_artwork, False, False, self.icon_missing_width, 0)
        return False, None, None

    @threads.glib_call
    def set_padding(self, padding):
        self.w_line.set_child_packing(
            self.w_artwork, False, False, padding, 0)
        return None

    @threads.glib_call
    def set_artwork(self, pix):
        self.w_artwork.set_from_pixbuf(pix)
        return None

    def create_widgets(self):
        items = [self.artist, self.album]
        artist = ' - '.join((x for x in items if x is not None))

        self.w_artwork = Gtk.Image()
        self.w_title = LabelWrap(self.name)
        self.w_artist = LabelWrap(artist)
        self.w_duration = Gtk.Label(self.duration)

        self.w_title.set_halign(Gtk.Align.START)
        self.w_artist.set_halign(Gtk.Align.START)

        self.w_artist.set_opacity(0.7)
        self.w_duration.set_opacity(0.7)

        contents = Gtk.VBox()
        contents.pack_start(self.w_title, False, False, 0)
        contents.pack_start(self.w_artist, False, False, 0)
        contents.set_halign(Gtk.Align.START)

        self.w_line = Gtk.HBox()
        self.w_line.pack_start(self.w_artwork, False, False, 10)
        self.w_line.pack_start(contents, False, False, 0)
        self.w_line.pack_end(self.w_duration, False, False, 10)

        spacer = Gtk.HSeparator()

        vbox = Gtk.VBox()
        vbox.pack_start(spacer, True, True, 0)
        vbox.pack_start(self.w_line, True, True, 10)

        self.add(vbox)
        return None

    @threads.glib_call
    def set_highlight(self, highlight, opacity=0.1):
        style = self.get_style_context()
        if highlight:
            _, c = style.lookup_color('fg_color')
            c.alpha = opacity
        else:
            _, c = style.lookup_color('bg_color')
        self.override_background_color(Gtk.StateFlags.NORMAL, c)
        return None

    def set_active(self, active):
        self.active = active
        if active:
            self.set_highlight(True, 0.15)
        else:
            self.set_highlight(False, 0.15)
        return None


class Playlist(Gtk.VBox):

    artwork_loaded = False
    load_artwork = False
    artwork_cache = {}
    timer = None

    def __init__(self, parent, artfolder):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings
        self.artfolder = artfolder

    def clicked(self, widget, *_):
        songid = widget.songid
        self.parent.client.play(songid)
        return None

    def add(self, widget, padding=0):
        self.pack_start(widget, True, True, padding)
        return None

    def set_active(self, current, previous):
        widgets = self.get_children()
        if previous is not None:
            widgets[previous].set_active(False)
        if current is not None:
            widgets[current].set_active(True)
        return None

    def populate(self, playlist):
        for widget in self.get_children():
            widget.destroy()
        icon_width = self.settings['icon_width']
        icon_missing_width = self.settings['icon_missing_width']
        music_folder = self.settings.get('mpd_music_directory', None)
        scrapers = self.settings.get('cover_order', None)
        scraper_regex = self.settings.get('cover_regex', None)
        for item in playlist:
            file_ = item.get('file', None)
            title = item.get('title', file_)
            album = item.get('album', None)
            artist = item.get('artist', None)
            duration = item.get('duration', 0)
            songid = item.get('pos')
            duration = timing.parse_time(float(duration))
            widget = PlaylistItem(title, artist, album, duration=duration,
                                  file_=file_,
                                  artwork_folder=self.artfolder,
                                  music_folder=music_folder,
                                  songid=songid,
                                  icon_width=icon_width,
                                  icon_missing_width=icon_missing_width,
                                  scrapers=scrapers,
                                  scraper_regex=scraper_regex)
            widget.connect('button-press-event', self.clicked)
            self.add(widget)
        return None

    @threads.threaded
    def fill_artwork(self):
        widgets = self.get_children()
        self.load_artwork = True
        self.artwork_loaded = False
        self.timer = GObject.timeout_add(500, self.set_artwork, widgets)
        return self.timer

    def halt_artwork(self):
        self.load_artwork = False
        return None

    @threads.threaded
    def set_artwork(self, widgets):
        LOGGER.debug('Starting playlist cover loading.')
        self._set_artwork(widgets, False)
        self._set_artwork(widgets, True)
        self.artwork_loaded = True
        self.load_artwork = False
        LOGGER.debug('Finished playlist cover loading.')
        return None

    def _set_artwork(self, widgets, online=True):
        for widget in widgets:
            if not self.load_artwork:
                break
            if widget.cover_loaded:
                continue
            from_cache, pixbuf, artwork = widget._draw(
                    self.artwork_cache, online)
            if not from_cache:
                self.artwork_cache[artwork] = pixbuf
                time.sleep(0.200)
                continue
            time.sleep(0.05)
        return None


class MainWindow(Gtk.Window):

    client = None
    idle_client = None
    song = None
    status = {}
    artwork = False
    click_toggle = False
    size = (300, 100)
    time = (time.time(), time.time() + 1)
    mouse_enter = False
    previous_song = None
    modes = {
        'persistent_player': True,
        'show_playlist': False,
        'player_overwrite': False,
    }

    def __init__(self, settings):
        super().__init__()
        self.set_title('impd')
        self.settings = settings
        self.create_widgets()
        self.connect('key-press-event', self._key_press)
        self.connect('enter-notify-event', self._mouse_enter)
        self.connect('leave-notify-event', self._mouse_leave)
        self.connect('delete-event', Gtk.main_quit)

    @property
    def playing(self):
        return self.status.get('state', None) == 'play'

    @property
    def stock_media(self):
        if not self.playing:
            return Gtk.STOCK_MEDIA_PLAY
        return Gtk.STOCK_MEDIA_PAUSE

    @property
    def current_song(self):
        song = self.client.currentsong()
        status = self.client.status()
        return (song, status)

    @property
    def player_overwrite(self):
        return self.modes.get('player_overwrite', False)

    @threads.glib_call
    def player_persistent(self, mode):
        if mode:
            self.w_cover.hide()
            self.modes['persistent_player'] = True
            self.w_player.set_opacity(1)
            height = self.w_player.get_allocated_height()
            width = self.settings['width']
            if self.modes['show_playlist']:
                height += 200
            self.size = (width, height)
            self.resize(width, height)
            return None
        if not self.player_overwrite:
            self.w_cover.hide()
        self.modes['persistent_player'] = self.player_overwrite
        self.w_player.set_opacity(int(self.mouse_enter))
        self.w_cover.show()
        return None

    def main(self):
        self.show_all()
        self.start_ticker()
        self.idle_ticker()
        Gtk.main()
        return None

    def create_widgets(self):
        # Artwork widget
        self.w_cover = Gtk.Image()
        self.w_cover.set_vexpand(True)
        e_cover = Gtk.EventBox()
        e_cover.add(self.w_cover)
        e_cover.connect('button-press-event', self._cover_clicked)

        # Time / Elapsed widgets
        self.w_elapsed = Gtk.Label('00:00')
        self.w_duration = Gtk.Label('-00:00')
        self.w_slider = Gtk.ProgressBar()
        self.w_slider.set_valign(Gtk.Align.CENTER)
        self.p_slider = Gtk.Alignment()
        self.p_slider.add(self.w_slider)
        self.p_slider.set_padding(10, 10, 0, 0)
        e_slider = Gtk.EventBox()
        e_slider.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        e_slider.add(self.p_slider)
        e_slider.connect('button-press-event', self._slider_clicked)
        e_slider.connect('motion-notify-event', self._slider_hover)

        time = Gtk.HBox()
        time.pack_start(self.w_elapsed, True, False, 10)
        time.pack_start(e_slider, True, True, 0)
        time.pack_start(self.w_duration, True, False, 10)

        # Play / pause
        self.w_playpause = Gtk.Image()
        self.w_playpause.set_from_stock(self.stock_media, 16)
        e_playpause = Gtk.EventBox()
        e_playpause.add(self.w_playpause)
        e_playpause.connect('button-press-event', self._playpause)

        # Previous
        self.w_previous = Gtk.Image()
        self.w_previous.set_from_stock(Gtk.STOCK_MEDIA_PREVIOUS, 16)
        e_previous = Gtk.EventBox()
        e_previous.add(self.w_previous)
        e_previous.connect('button-press-event', self._previous)

        # Next
        self.w_next = Gtk.Image()
        self.w_next.set_from_stock(Gtk.STOCK_MEDIA_NEXT, 16)
        e_next = Gtk.EventBox()
        e_next.add(self.w_next)
        e_next.connect('button-press-event', self._next)

        # Menu
        self.w_toggleplaylist = Gtk.Image()
        self.w_toggleplaylist.set_from_stock(Gtk.STOCK_ADD, 16)
        e_toggleplaylist = Gtk.EventBox()
        e_toggleplaylist.add(self.w_toggleplaylist)
        e_toggleplaylist.connect('button-press-event', self._toggle_playlist)

        # Controls
        controls = Gtk.HBox()
        controls.pack_start(e_previous, True, True, 10)
        controls.pack_start(e_playpause, True, True, 10)
        controls.pack_end(e_toggleplaylist, False, False, 10)
        controls.pack_end(e_next, True, True, 10)

        # Player Section
        style = self.get_style_context()
        _, background = style.lookup_color('bg_color')

        self.w_player = Gtk.VBox()
        self.w_player.pack_start(time, False, False, 10)
        self.w_player.pack_start(controls, False, False, 10)
        self.w_player.set_valign(Gtk.Align.END)
        self.w_player.override_background_color(
            Gtk.StateFlags.NORMAL,
            background)

        # Overlay

        overlay = Gtk.Overlay()
        overlay.add_overlay(e_cover)
        overlay.add_overlay(self.w_player)
        overlay.set_hexpand(True)
        overlay.set_vexpand(True)

        # Playlist
        width = self.settings['width']
        folder = self.settings['artwork_folder']

        self.w_playlist = Playlist(self, folder)
        s_playlist = Gtk.ScrolledWindow()
        s_playlist.add(self.w_playlist)
        s_playlist.set_size_request(width, 200)
        s_playlist.set_max_content_width(width)
        s_playlist.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        self.s_playlist = s_playlist

        # Add all the widgets
        
        self.vbox = Gtk.VBox()
        self.vbox.set_homogeneous(False)
        self.vbox.pack_start(overlay, True, True, 0)
        # self.vbox.pack_start(s_playlist, False, False, 0)

        self.add(self.vbox)
        return None

    def _cover_clicked(self, *_):
        self.click_toggle = not self.click_toggle
        self.modes['persistent_player'] = self.click_toggle
        self.modes['player_overwrite'] = self.click_toggle
        if self.click_toggle:
            self.w_player.set_opacity(
                self.settings.get('player_opacity') / 100)
        return None

    def _key_press(self, widget, event):
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)
        if keyname == 'space':
            self._playpause()
        return None

    def _slider_hover(self, widget, event):
        xpos = event.x
        width = widget.get_allocated_width()
        percent = xpos / width
        time = percent * float(self.song.get('duration', 0))
        parsed_time = timing.parse_time(time)
        self.p_slider.set_tooltip_text(parsed_time)
        return None

    def _slider_clicked(self, widget, event):
        xpos = event.x
        width = widget.get_allocated_width()
        percent = xpos / width
        time = percent * float(self.song.get('duration', 0))
        self.client.seekcur(time)
        return None

    def _playpause(self, *_):
        state = int(self.playing)
        self.client.pause(state)
        self.w_playpause.set_from_stock(self.stock_media, 16)
        return None

    def _previous(self, *_):
        self.client.previous()
        return None

    def _next(self, *_):
        self.client.next()
        return None

    def _toggle_playlist(self, *_, force=None):
        show = force or not self.modes['show_playlist']
        self.modes['show_playlist'] = show
        if not show:
            self.vbox.remove(self.s_playlist)
            width, height = self.size
            self.size = (width, height - 200)
            self.resize(*self.size)
            self.w_playlist.halt_artwork()
            self.w_toggleplaylist.set_from_stock(Gtk.STOCK_ADD, 16)
        else:
            self.vbox.pack_start(self.s_playlist, False, False, 0)
            self.s_playlist.show_all()
            width, height = self.size
            self.size = (width, height + 200)
            self.resize(*self.size)
            self.w_playlist.fill_artwork()
            self.w_toggleplaylist.set_from_stock(Gtk.STOCK_REMOVE, 16)
        return None

    def _mouse_enter(self, *_):
        LOGGER.debug('Mouse enter ->')
        if self.modes['persistent_player']:
            self.mouse_enter = True
            return None
        opacity = self.settings['player_opacity']
        if not self.mouse_enter:
            self.fade(self.w_player, 0, int(opacity), self.settings['fade_in'])
        self.mouse_enter = True
        return None

    def _mouse_leave(self, *_):
        LOGGER.debug('Mouse leave <-')
        if self.modes['persistent_player']:
            self.mouse_enter = False
            return None
        opacity = self.settings['player_opacity']
        delay = abs(self.settings['fade_out'])
        delay = delay - (delay * 2)
        if self.mouse_enter:
            self.fade(self.w_player, int(opacity), 0, delay)
        self.mouse_enter = False
        return None

    @threads.threaded
    def fade(self, widget, start, finish, step):
        for i in range(start, finish, step):
            self._fade(widget, i/100)
            time.sleep(0.01)
        self._fade(widget, finish/100)
        return None

    @threads.glib_call
    def _fade(self, widget, value):
        widget.set_opacity(value)
        return None

    def mpd_connect(self):
        host = self.settings['host']
        port = self.settings['port']
        connection = client.Client()
        connection.connect(host, port)
        return connection

    def check_connections(self):
        if self.client is None:
            self.client = self.mpd_connect()
            return True
        return False

    def check_cover(self, song, online=True):
        cover = self.find_cover(self.song, online=online)
        if self.song != song:
            return None
        self.update_cover(cover)
        return None

    def find_cover(self, song, online=True):
        if song.get('file', None) is None:
            return None
        LOGGER.debug('Finding cover: {}'.format(song['file']))
        folder = self.settings['artwork_folder']
        mpd_folder = self.settings.get('mpd_music_directory', None)
        if mpd_folder is not None:
            mpd_folder = os.path.expanduser(mpd_folder)
        file = song.get('file')
        artist = song.get('artist', None)
        title = song.get('title', file)
        album = song.get('album', None)
        scrapers = self.settings.get('cover_order', [])
        scraper_regex = self.settings.get('cover_regex', None)
        path = cover.find_artwork(title, album, artist, folder, mpd_folder,
                                  scrapers, online=online, filepath=file,
                                  scraper_regex=scraper_regex)
        return path

    def find_playlist(self):
        playlist = self.client.playlistinfo()
        self.update_playlist(playlist)
        return playlist

    @threads.glib_call
    def update_cover(self, artwork):
        self.artwork = artwork
        width = self.settings['width']

        if artwork is None:
            self.player_persistent(True)
            return None

        LOGGER.debug('Setting cover: {}'.format(artwork))

        if not self.modes['player_overwrite']:
            self.player_persistent(False)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            artwork,
            width, -1,
            preserve_aspect_ratio=True)

        self.w_cover.set_from_pixbuf(pixbuf)
        image_height = pixbuf.get_height()

        playlist = self.modes['show_playlist']
        if playlist:
            image_height += 200
        self.resize(width, image_height)
        self.size = (width, image_height)

        songfile = self.song.get('file', 'None')
        songname = self.song.get('title', songfile)
        songartist = self.song.get('artist', 'None')
        self.w_cover.set_tooltip_text('{} - {}'.format(songname, songartist))
        return None

    @threads.glib_call
    def update_time(self):
        stopped = self.status.get('state', 'stop') == 'stop'
        if stopped:
            return None
        start, end = self.time
        if not self.playing:
            elapsed = float(self.status['elapsed'])
        else:
            elapsed = time.time() - start
        duration = end - start
        progress = elapsed / duration
        f_elapsed = timing.parse_time(elapsed)
        f_duration = timing.parse_time(abs(elapsed - duration))
        self.w_slider.set_fraction(progress)
        self.w_elapsed.set_text(f_elapsed)
        self.w_duration.set_text('-{}'.format(f_duration))
        return None

    @threads.glib_call
    def update_playlist(self, playlist):
        self.w_playlist.populate(playlist)
        return None

    @threads.glib_call
    def update_playpause(self):
        self.w_playpause.set_from_stock(self.stock_media, 16)
        return None

    @threads.glib_call
    def update_current(self):
        song = self.song
        pos = int(song.get('pos', None))
        if pos is not None:
            self.w_playlist.set_active(pos, self.previous_song)
            self.previous_song = pos
        return None

    @threads.glib_call
    def check_size(self):
        self.resize(*self.size)
        return None

    @threads.threaded
    def idle_ticker(self):
        idle = self.mpd_connect()
        while True:
            systems = idle.idle('player', 'mixer', 'playlist')
            if systems is None:
                idle = self.mpd_connect()
                continue
            for system in systems:
                func = getattr(self, '_idle_{}'.format(system), None)
                if func is not None:
                    LOGGER.debug('Calling self._idle_{}()'.format(system))
                    func()
        return None

    def attempt_connections(self, attempts=10):
        for i in range(attempts):
            LOGGER.debug('Attempting to connect.')
            connected = self.check_connections()
            if connected:
                return True
        return False

    @threads.threaded
    def start_ticker(self):
        connected = False
        while not connected:
            connected = self.attempt_connections()
            LOGGER.debug('Could not connect.')

        playlist = self.client.playlistinfo()
        self.update_playlist(playlist)
        # self.w_playlist.populate(self.client.playlistinfo())

        self.song, self.status = self.current_song
        if self.status['state'] != 'stop':
            self.time = parse_time(self.status)
            self.check_cover(self.song)
        self.w_playpause.set_from_stock(self.stock_media, 16)
        self.update_current()

        update_interval = self.settings['update_interval']
        for i in itertools.cycle(range(10)):
            self.update_time()
            if i % 5 == 0:
                self.check_size()
            time.sleep(update_interval)
        return None

    def _idle_player(self):
        self.song, self.status = self.current_song
        if self.status.get('state', 'stop') == 'stop':
            # Clear the UI
            return None
        self.time = parse_time(self.status)
        self.check_cover(self.song)
        self.update_playpause()
        self.update_current()
        return None

    @threads.glib_call
    def _idle_playlist(self):
        self.w_playlist.halt_artwork()
        playlist = self.client.playlistinfo()
        self.w_playlist.populate(playlist)
        self.w_playlist.fill_artwork()
        return None


def parse_time(status):
    now = time.time()
    elapsed = float(status['elapsed'])
    duration = float(status['duration'])
    start = now - elapsed
    end = start + duration
    return (start, end)

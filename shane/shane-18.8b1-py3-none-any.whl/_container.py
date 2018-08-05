import math
import os
import subprocess as sp

from shane._streams import create_stream_from_ffprobe

from ._ffmpeg import FFmpegCompressor, FFprobe
from ._utils import SUPPORTED_VIDEO_EXTENTIONS


def create_container_from_ffprobe(ffprobe_format: dict, ffprobe_streams: list, 
    ffprobe_chapters: list):
    return Container(
        ffprobe_format=ffprobe_format,
        ffprobe_streams=ffprobe_streams,
        ffprobe_chapters=ffprobe_chapters
        )


class Container:
    """A Container wraps a file that contains several multimedia 
    streams"""
    def __init__(self, *streams, **kwargs) -> None:
        self._init_with_ffprobe(
            ffprobe_format=kwargs.get("ffprobe_format", {}), 
            ffprobe_streams=kwargs.get("ffprobe_streams", []),
            ffprobe_chapters=kwargs.get("ffprobe_chapters", []), 
        )
        self._streams += [s for s in streams]
    
    def _init_with_ffprobe(self, ffprobe_format: dict, ffprobe_streams: list, 
        ffprobe_chapters: list) -> None:
        self._streams = []
        self._init_with_ffprobe_format(ffprobe_format)
        self._init_with_ffprobe_streams(ffprobe_streams)
        self._init_with_ffprobe_chapters(ffprobe_chapters)
    
    def _init_with_ffprobe_format(self, ffprobe_format: dict) -> None:
        self._ffprobe_format = ffprobe_format
        self._default_ffprobe_format = ffprobe_format.copy()

    def _init_with_ffprobe_streams(self, ffprobe_streams: list) -> None:
        for ffprobe_stream in ffprobe_streams:
            stream = create_stream_from_ffprobe(
                ffprobe_stream=ffprobe_stream, 
                ffprobe_format={},
                container=self)
            self._streams.append(stream)

    def _init_with_ffprobe_chapters(self, ffprobe_chapters: list) -> None:
        self._ffprobe_chapters = ffprobe_chapters
        self._default_ffprobe_chapters = ffprobe_chapters.copy()
    
    def __repr__(self) -> str:
        path = self.path
        size = self.human_size
        duration = self.human_duration
        return f"Container(path={path}, size={size}, duration={duration})"

    @property
    def metadata(self):
        return self._ffprobe_format.get("tags")

    @property
    def path(self) -> str:
        """The path to the file that is wrapped by the Container"""
        return self._ffprobe_format.get("filename")
    
    @property
    def is_container(self) -> bool:
        return isinstance(self, Container)
    
    @property
    def extention(self) -> str:
        """The file extention."""
        if self.path:
            return os.path.splitext(self.path)[-1]
        else:
            return None

    @property
    def format(self):
        """The container format name"""
        return self._ffprobe_format.get("format_name")

    @property
    def size(self) -> int:
        """The file size in bytes"""
        size = self._ffprobe_format.get("size")
        return int(size) if size else None
 
    @property
    def human_size(self) -> str:
        """The human-readable file size."""
        if self.size is None:
            return None
        if self.size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(self.size, 1024)))
        p = math.pow(1024, i)
        s = round(self.size / p, 2)
        return f"{s} {size_name[i]}"
    
    @property
    def bitrate(self) -> int:
        """The number of bits processed per second"""
        bit_rate = self._ffprobe_format.get("bit_rate")
        return int(bit_rate) if bit_rate else None

    @property
    def duration(self) -> float:
        """The duration in seconds"""
        duration = self._ffprobe_format.get("duration")
        return float(duration) if duration else None
    
    @property
    def human_duration(self) -> str:
        """The human-readable duration."""
        if self.duration is None:
            return None
        minutes, seconds = divmod(self.duration, 60)
        hours, _ = divmod(minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"    
    
    @property
    def start_time(self) -> float:
        start_time = self._ffprobe_format.get("start_time")
        return float(start_time) if start_time else start_time

    @property
    def streams(self) -> tuple:
        return tuple(self._streams)
      
    @property
    def videos(self) -> tuple:
        """All video streams in the container"""
        return tuple([stream for stream in self.streams if stream.is_video])

    @property
    def audios(self) -> tuple:
        """All audio streams in the container"""
        return tuple([stream for stream in self.streams if stream.is_audio])

    @property
    def subtitles(self) -> tuple:
        """All subtitle streams in the container"""
        return tuple([stream for stream in self.streams if stream.is_subtitle])

    @property
    def data(self) -> tuple:
        """All data streams in the container"""
        return tuple([stream for stream in self.streams if stream.is_data])    

    @property
    def attachments(self) -> tuple:
        """All attachment streams in the container"""
        return tuple([stream for stream in self.streams if stream.is_attachment])    

    @property
    def images(self) -> tuple:
        """All image streams in the container"""
        return tuple([stream for stream in self.streams if stream.is_image])    

    @property
    def default_extention(self) -> str:
        """The file extention."""
        if self.default_path:
            return os.path.splitext(self.default_path)[-1]
        else:
            return None    
    
    @property
    def default_path(self) -> str:
        """The default path to the file that is wrapped by the Container"""
        return self._default_ffprobe_format.get("filename")
        
    @path.setter
    def path(self, path: str):
        """Property setter for self.path."""
        if os.path.exists(path):
            raise ValueError(f"The path '{path}' already exists")
        else:
            self._ffprobe_format['filename'] = path

    @extention.setter
    def extention(self, x: str):
        """Property setter for self.extention."""
        if self.path is None:
            raise ValueError(
                f"Can't add the extention to the path: {self.path}"
            )
        if x in SUPPORTED_VIDEO_EXTENTIONS:
            self.path = os.path.splitext(self.path)[0] + x
        else:
            ValueError(f"The extention '{x}' is not supported.")
    
    def add_stream(self, stream) -> None:
        self._streams.append(stream)

    def remove_stream(self, stream) -> None:
        self._streams.remove(stream)

    def remove_streams_if(self, function) -> None:
        """Removes streams for which function returns true"""
        self._streams = [s for s in self._streams if not function(s)]

    def set_metadata(self, key, value):
        self._ffprobe_format["tags"][key] = value

    def del_metadata(self, key):
        del self._ffprobe_format["tags"][key]

    def _get_all_input_files(self):
        if self.default_path is not None:
            # self container + outer streams
            return [self] + [s for s in self.streams if not s.inner]
        else:
             # only outer streams
            return [s for s in self.streams if not s.inner]
    
    def save(self, **settings) -> int:
        compressor = FFmpegCompressor()
        compressor.add_input_files(*self._get_all_input_files())
        compressor.add_output_path(self.path)
        compressor.add_settings(**settings)
        response = compressor.run()
        ffprobe = FFprobe(self.path)
        self._init_with_ffprobe(
            ffprobe_format=ffprobe.get_format(),
            ffprobe_chapters=ffprobe.get_chapters(),
            ffprobe_streams=ffprobe.get_streams(),
        )
        return response

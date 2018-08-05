import os
import subprocess as sp
from pathlib import Path

from ._ffmpeg import FFprobe, FFmpegCompressor
from ._utils import (
    IMAGES_CODECS, 
    
    SUPPORTED_AUDIO_EXTENTIONS,
    SUPPORTED_SUBTITLE_EXTENTIONS,
    SUPPORTED_VIDEO_EXTENTIONS,    
)



class StreamError(Exception):
    pass



def choose_stream_class(codec_type, codec_name):
    if codec_type == "video":
        if codec_name in IMAGES_CODECS:
            return ImageStream
        return VideoStream
    elif codec_type == "audio":
        return AudioStream
    elif codec_type == "subtitle":
        return SubtitleStream
    elif codec_type == "data":
        return DataStream
    elif codec_type == "attachment":
        return AttachmentStream
    else:
        raise ValueError("Invalid Stream")


def create_stream_from_ffprobe(
        ffprobe_stream: dict, 
        ffprobe_format={}, 
        container=None):
    codec_type = ffprobe_stream["codec_type"]
    codec_name = ffprobe_stream["codec_name"]
    stream_class = choose_stream_class(codec_type, codec_name)
    return stream_class(
        ffprobe_stream=ffprobe_stream,
        ffprobe_format=ffprobe_format,
        container=container,
    )



class Stream:
    """A base class of the streams."""
    def __init__(self, ffprobe_stream: dict, ffprobe_format: dict, container):
        self._init_from_ffprobe(ffprobe_stream, ffprobe_format, container)

    def _init_from_ffprobe(self, ffprobe_stream, ffprobe_format, container):
        # if it is an inner stream than ffprobe_format is an empty dict
        self._ffprobe_format = ffprobe_format
        self._default_ffprobe_format = ffprobe_format.copy()

        self._ffprobe_stream_info = ffprobe_stream
        self._default_ffprobe_stream_info = ffprobe_stream.copy()

        self.container = container

    @property
    def metadata(self):
        return self._ffprobe_stream_info["tags"]
    
    @property
    def is_container(self) -> bool:
        return not isinstance(self, Stream)

    @property
    def is_stream(self) -> bool:
        return isinstance(self, Stream)

    @property
    def path(self) -> str:
        """The path to the file, if the stream is not inner."""
        return self._ffprobe_format.get("filename")

    @property
    def extention(self):
        """The stream extention."""
        if self.path:
            return Path(self.path).suffix
        else:
            return None

    @property
    def index(self) -> int:
        """The stream index in the container."""
        return self._ffprobe_stream_info["index"]

    @property
    def inner(self) -> bool:
        """Indicates whether the stream is some container or not"""
        return self.container is not None

    @property
    def codec(self) -> str:
        """The stream codec."""
        return self._ffprobe_stream_info["codec_name"]

    @property
    def type(self) -> str:
        """The common type of the stream."""
        return self._ffprobe_stream_info["codec_type"]
    
    @property
    def is_video(self) -> bool:
        return (self.type == "video") and (self.codec not in IMAGES_CODECS)

    @property
    def is_audio(self) -> bool:
        return self.type == "audio"

    @property
    def is_subtitle(self) -> bool:
        return self.type == "subtitle"

    @property
    def is_data(self) -> bool:
        return self.type == "data"

    @property
    def is_attachment(self) -> bool:
        return self.type == 'attachment'

    @property
    def is_image(self) -> bool:
        return (self.type == "video") and (self.codec in IMAGES_CODECS)
    
    @property
    def is_default(self) -> bool:
        """Specifies whether the stream is the default stream"""
        return self._ffprobe_format["disposition"]["default"] == 1

    @property
    def default_codec(self):    
        return self._default_ffprobe_stream_info["codec_name"]
    
    @property
    def default_path(self):
        """The path to the file, if the stream is not inner."""
        return self._default_ffprobe_format.get("filename")

    @property
    def default_extention(self):
        """The stream extention."""
        if self.default_path:
            return Path(self.default_path).suffix
        else:
            return None
    
    @path.setter
    def path(self, path):
        """Property setter for self.path."""
        if self.inner == True:
            raise AttributeError("An inner stream can not have a path")
        if Path(path).exists():
            raise ValueError(f"The path '{path}' already exists")
        self._ffprobe_format["filename"] = path

    @extention.setter
    def extention(self, ext: str):
        """Property setter for self.extention."""
        if self.inner == True:
            raise AttributeError("An inner stream can not have an extention")
        if self.is_video:
            supported_extentions = SUPPORTED_VIDEO_EXTENTIONS
        elif self.is_audio:
            supported_extentions = SUPPORTED_AUDIO_EXTENTIONS
        elif self.is_subtitle:
            supported_extentions = SUPPORTED_SUBTITLE_EXTENTIONS
        else:
            raise NotImplementedError # TODO
        if ext in supported_extentions:
            root, _ = os.path.splitext(self.path)
            self.path = root + ext
        else:
            raise ValueError(f"The extention '{ext}' is not supported.")

    @codec.setter
    def codec(self, value: str):
        """Property setter for self.codec."""
        error = f"The codec '{value}' is not supported."
        if self.is_video:
            if value in SUPPORTED_VIDEO_CODECS:
                self._ffprobe_stream_info["codec_name"] = value
            else:
                raise ValueError(error)
        elif self.is_audio:
            if value in SUPPORTED_AUDIO_CODECS:
                self._ffprobe_stream_info["codec_name"] = value
            else:
                raise ValueError(error)
        elif self.is_subtitle:
            if value in SUPPORTED_SUBTITLE_CODECS:
                self._ffprobe_stream_info["codec_name"] = value
            else:
                raise ValueError(error)
        else:
            raise ValueError(error)
    
    @is_default.setter
    def is_default(self, value: bool):
        """Property setter for self.is_default."""
        return bool(self._ffprobe_format["disposition"]["default"])

    def save(self, **settings):
        """Saves all the changes. Only for outer streams"""
        if self.inner:
            raise StreamError(
                'You can not save an inner stream. You can only extract it.'
            )
        compressor = FFmpegCompressor()
        compressor.add_input_files(self)
        compressor.add_output_path(self.path)
        compressor.add_settings(**settings)
        response = compressor.run()
        ffprobe = FFprobe(path)
        self._init_from_ffprobe(
            ffprobe.get_first_stream(),
            ffprobe.get_format(),
            container
        )
        return response

    def extract(self, path=None, **settings):
        """Extreacts the stream and saves it to the `path`. Returns 
         the extracted stream"""
        if not self.inner:
            raise StreamError(
                'You can not extract an outer stream. You can only save it.'
            )
        compressor = FFmpegCompressor()
        compressor.add_input_files(self.container)
        compressor.add_output_path(path)
        compressor.add_settings(**settings)
        compressor.extract_stream_run(self)
        ffprobe = FFprobe(path)
        return create_stream_from_ffprobe(
            ffprobe.get_first_stream(),
            ffprobe.get_format(),
            None,
        )



class VideoStream(Stream):
    """A video stream.""" 
    def _init_from_ffprobe(self, ffprobe_stream, ffprobe_format, container):
        Stream._init_from_ffprobe(self, ffprobe_stream, ffprobe_format, container)
        fps = self._default_ffprobe_stream_info.get("avg_frame_rate")
        if fps is not None and fps != '0/0':
            self._default_ffprobe_stream_info["avg_frame_rate"] = \
            self._ffprobe_stream_info["avg_frame_rate"] = \
            eval(self._default_ffprobe_stream_info["avg_frame_rate"])
        else:
            self._default_ffprobe_stream_info["avg_frame_rate"] = 0
            self._ffprobe_stream_info["avg_frame_rate"] = 0

    
    # @property
    # def bitrate(self) -> int: # TODO
    #     """The number of bits processed per second."""
    #     raise NotImplementedError

    @property
    def fps(self) -> int:
        """A number of frames per second."""
        return self._ffprobe_stream_info["avg_frame_rate"]

    @property
    def width(self) -> int:
        """The width of the the video."""
        return self._ffprobe_stream_info["width"]

    @property
    def height(self) -> int:
        """The height of the the video."""
        return self._ffprobe_stream_info["height"]

    @fps.setter
    def fps(self, value: float): 
        """Property setter for self.fps."""
        if isinstance(value, float) or isinstance(value, int):
            self._ffprobe_stream_info["avg_frame_rate"] = value
        else:
            raise TypeError("The fps value must be a number.")

    @property
    def default_fps(self):
        return self._default_ffprobe_stream_info["avg_frame_rate"]
    
    @property
    def default_width(self) -> int:
        """The default width of the the video."""
        return self._default_ffprobe_stream_info["width"]

    @property
    def default_height(self) -> int:
        """The default height of the the video."""
        return self._default_ffprobe_stream_info["height"]

    @width.setter
    def width(self, value: int):
        """Property setter for self.width."""
        if isinstance(value, int):
            self._ffprobe_stream_info["width"] = value
        else:
            raise TypeError("The width value must be an integer.")

    @height.setter
    def height(self, value: int):
        """Property setter for self.height."""
        if isinstance(value, int):
            self._ffprobe_stream_info["height"] = value
        else:
            raise TypeError("The height value must be an integer.")

    def __repr__(self):
        return (self.__class__.__name__ + "("
            f"path={self.path}, codec={self.codec}, fps={self.fps}, " + 
            f"width={self.width}, height={self.height}, " +
            f"language={self.metadata.get('language')}" +
            ")"
        )



class AudioStream(Stream):
    """An audio stream."""
    @property
    def channels(self) -> int:
        """The number of channels."""
        return int(self._ffprobe_stream_info["channels"])

    @property
    def sample_rate(self) -> float:
        """The audio sample rate."""
        return float(self._ffprobe_stream_info["sample_rate"])

    # TODO @sample_rate.setter
    # TODO @channels.setter

    def __repr__(self):
        return (self.__class__.__name__ + "("
            f"path={self.path}, codec={self.codec}, channels={self.channels}, " + 
            f"sample_rate={self.sample_rate}, " +
            f"language={self.metadata.get('language')}" +
            ")"
        )



class SubtitleStream(Stream):
    """A subtitle stream."""

    @property
    def is_forced(self) -> bool:
        """Specifies whether subtitles are forced or not."""
        return self._ffprobe_format["disposition"]["forced"] == 1

    @is_forced.setter
    def is_forced(self, value: bool):
        """Property setter for self.is_forced."""
        self._ffprobe_format["disposition"]["forced"] = 1 if value is True else 0 

    def __repr__(self):
        return (self.__class__.__name__ + "("
            f"path={self.path}, codec={self.codec}, is_forced={self.is_forced}, " + 
            f"language={self.metadata.get('language')}" +
            ")"
        )



class DataStream(Stream): # ?
    def __repr__(self):
        return (self.__class__.__name__ + "("
            f"path={self.path}, codec={self.codec}, " + 
            ")"
        )



class ImageStream(Stream): # ?
    def __repr__(self):
        return (self.__class__.__name__ + "("
            f"path={self.path}, codec={self.codec}, " + 
            ")"
        )



class AttachmentStream(Stream): # ?
    def __repr__(self):
        return (self.__class__.__name__ + "("
            f"path={self.path}, codec={self.codec}, " + 
            f"language={self.metadata.get('language')}" +
            ")"
        )

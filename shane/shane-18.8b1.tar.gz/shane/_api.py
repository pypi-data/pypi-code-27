from pathlib import Path
from shane._container import create_container_from_ffprobe
from shane._streams import create_stream_from_ffprobe
from shane._ffmpeg import FFprobe


__all__ = ['open']


def open(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"The path '{path}' doesn't exists.")
    else:
        ffprobe = FFprobe(path)
        
        ffprobe_format = ffprobe.get_format()
        ffprobe_streams = ffprobe.get_streams()
        ffprobe_chapters = ffprobe.get_chapters()

        if len(ffprobe_streams) == 1:
            return create_stream_from_ffprobe(
                ffprobe_format=ffprobe_format,
                ffprobe_stream=ffprobe_streams[0],
            )
        else:
            return create_container_from_ffprobe(
                ffprobe_format=ffprobe_format,
                ffprobe_chapters=ffprobe_chapters,
                ffprobe_streams=ffprobe_streams,
            )

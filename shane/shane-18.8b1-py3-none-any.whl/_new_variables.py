
# Можно автоматически?
# Можно смотреть в ffmpeg -formats и ffmpeg -h muxer=entry
# Тогда для каждого формата выбирать default кодек! Если default кодек
# совпадает, то использовать copy.

# Но для ".mkv", ".m4v", ".mp4" добавить полную поддержку всех кодеков


DEFAULT_VIDEO_CODEC_FOR_FORMAT = {
    # взять пропарсив ffmpeg -h muxer=entry
}
DEFAULT_AUDIO_CODEC_FOR_FORMAT = {
    # взять пропарсив ffmpeg -h muxer=entry
}
DEFAULT_SUBTITLE_CODEC_FOR_FORMAT = {
    # взять пропарсив ffmpeg -h muxer=entry
} # + {"mov_text" for mp4 and m4v}


# shane can convert only to...
SUPPORTED_VIDEO_EXTENTIONS = [".mkv", ".m4v", ".mp4",]
SUPPORTED_AUDIO_EXTENTIONS = [".aac", ".ac3",]
SUPPORTED_SUBTITLE_EXTENTIONS = [".srt",]


CONTAINER_VIDEO_CODEC_SUPPORT = {
    ".mkv": [],
    ".m4v": [],
    ".mp4": [],
    ".webm": [],
    ".avi": [],
}

CONTAINER_AUDIO_CODEC_SUPPORT = {
    ".mkv": [],
    ".m4v": [],
    ".mp4": [],
    ".webm": [],
    ".avi": [],
}

CONTAINER_SUBTITLE_CODEC_SUPPORT = {
    ".mkv": [],
    ".m4v": [],
    ".mp4": [],
    ".webm": [],
}
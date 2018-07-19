import json
import subprocess
import shutil

from transcoded.struct import VideoMetadata, AudioStream, SubtitleStream


def probe_file(filename):
    if shutil.which('ffprobe') is not None:
        return probe_ffmpeg(filename)
    if shutil.which('avprobe') is not None:
        return probe_libav(filename)
    raise ValueError('Ffmpeg or libav not installed')


def probe_ffmpeg(filename):
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', filename]
    result = subprocess.check_output(command)
    data = json.loads(result.decode('utf-8'))
    result = VideoMetadata()
    result.container = data['format']['format_name']
    result.container_long = data['format']['format_long_name']
    result.length = int(float(data['format']['duration']))
    result.bitrate = int(float(data['format']['bit_rate']))

    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            result.video.codec = stream['codec_name']
            result.video.codec_long = stream['codec_long_name']
            if 'bit_rate' in stream:
                result.video.bitrate = int(float(stream['bit_rate']))
            result.video.width = int(stream['width'])
            result.video.height = int(stream['height'])

        if stream['codec_type'] == 'audio':
            audio = AudioStream()
            audio.codec = stream['codec_name']
            audio.codec_long = stream['codec_long_name']
            audio.channels = int(stream['channels'])
            if 'bit_rate' in stream:
                audio.bitrate = int(float(stream['bit_rate']))
            if 'tags' in stream:
                if 'language' in stream['tags']:
                    audio.language = stream['tags']['language']
                if 'title' in stream['tags']:
                    audio.title = stream['tags']['title']
            result.audio.append(audio)

        if stream['codec_type'] == 'subtitle':
            sub = SubtitleStream()
            sub.codec = stream['codec_name']
            sub.codec_long = stream['codec_long_name']
            if 'tags' in stream:
                if 'language' in stream['tags']:
                    sub.language = stream['tags']['language']
                if 'title' in stream['tags']:
                    sub.title = stream['tags']['title']
            result.subtitles.append(sub)
    return result


def probe_libav(filename):
    command = ['avprobe', '-v', 'quiet', '-of', 'json', '-show_format', '-show_streams', filename]
    result = subprocess.check_output(command)
    data = json.loads(result.decode('utf-8'))
    result = VideoMetadata()
    result.container = data['format']['format_name']
    result.container_long = data['format']['format_long_name']
    result.length = int(float(data['format']['duration']))
    result.bitrate = int(float(data['format']['bit_rate']))

    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            result.video.codec = stream['codec_name']
            result.video.codec_long = stream['codec_long_name']
            if 'bit_rate' in stream:
                result.video.bitrate = int(float(stream['bit_rate']))
            result.video.width = int(stream['width'])
            result.video.height = int(stream['height'])

        if stream['codec_type'] == 'audio':
            audio = AudioStream()
            audio.codec = stream['codec_name']
            audio.codec_long = stream['codec_long_name']
            audio.channels = int(stream['channels'])
            if 'bit_rate' in stream:
                audio.bitrate = int(float(stream['bit_rate']))
            if 'tags' in stream:
                if 'language' in stream['tags']:
                    audio.language = stream['tags']['language']
                if 'title' in stream['tags']:
                    audio.title = stream['tags']['title']
            result.audio.append(audio)

        if stream['codec_type'] == 'subtitle':
            sub = SubtitleStream()
            sub.codec = stream['codec_name']
            sub.codec_long = stream['codec_long_name']
            if 'tags' in stream:
                if 'language' in stream['tags']:
                    sub.language = stream['tags']['language']
                if 'title' in stream['tags']:
                    sub.title = stream['tags']['title']
            result.subtitles.append(sub)
    return result

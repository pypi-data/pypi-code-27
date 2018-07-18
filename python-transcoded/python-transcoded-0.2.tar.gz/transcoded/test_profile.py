from unittest import TestCase
from transcoded.profile import Profile
from transcoded.struct import VideoMetadata


class TestProfile(TestCase):
    def test__parse_bitrate(self):
        tests = [
            ['0', 0],
            ['1', 1],
            ['999999', 999999],
            ['1k', 1024],
            ['1K', 1024],
            ['1m', 1048576],
            ['1.5M', 1572864]
        ]
        for test in tests:
            temp = Profile('test', '')
            result = temp._parse_bitrate(test[0])
            self.assertEqual(test[1], result, msg='Parsing {}'.format(test[0]))

    def test_cmdline_ffmpeg(self):
        profile_raw = {}
        metadata = VideoMetadata()
        profile = Profile('test', profile_raw)
        result = profile.cmdline_ffmpeg('a', 'b', metadata)
        self.assertListEqual(['-i', 'a', '-vcodec', 'copy', '-acodec', 'copy', '-f', 'mkv', 'b'], result)

        profile_raw = {
            'container': 'mp4',
            'vcodec': 'h264'
        }
        profile = Profile('test', profile_raw)
        result = profile.cmdline_ffmpeg('a', 'b', metadata)
        self.assertListEqual(
            ['-i',
             'a',
             '-vcodec',
             'libx264',
             '-preset',
             'medium',
             '-profile',
             'main',
             '-pix_fmt',
             'yuv420p',
             '-acodec',
             'copy',
             '-f',
             'mp4',
             'b'], result)

        profile_raw = {
            'container': 'mp4',
            'vcodec': 'h264',
            'h264_crf': '18'
        }
        profile = Profile('test', profile_raw)
        result = profile.cmdline_ffmpeg('a', 'b', metadata)
        self.assertListEqual(
            ['-i',
             'a',
             '-vcodec',
             'libx264',
             '-preset',
             'medium',
             '-profile',
             'main',
             '-crf',
             '18',
             '-pix_fmt',
             'yuv420p',
             '-acodec',
             'copy',
             '-f',
             'mp4',
             'b'], result)

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

    def test_cmdline_ffmpeg_defaults(self):
        expected = ['-y', '-i', 'a', '-vcodec', 'copy', '-acodec', 'copy', '-f', 'matroska', 'b']
        self._test_profile({}, expected)

    def test_cmdline_ffmpeg_mp4_h264(self):
        profile_raw = {
            'container': 'mp4',
            'vcodec': 'h264'
        }
        expected = ['-y',
                    '-i',
                    'a',
                    '-vcodec',
                    'libx264',
                    '-preset',
                    'medium',
                    '-profile:v',
                    'main',
                    '-pix_fmt',
                    'yuv420p',
                    '-acodec',
                    'copy',
                    '-f',
                    'mp4',
                    'b']
        self._test_profile(profile_raw, expected)

    def test_cmdline_ffmpeg_mp4_h264_crf(self):
        profile_raw = {
            'container': 'mp4',
            'vcodec': 'h264',
            'h264_crf': '18'
        }
        expected = ['-y',
                    '-i',
                    'a',
                    '-vcodec',
                    'libx264',
                    '-preset',
                    'medium',
                    '-profile:v',
                    'main',
                    '-crf',
                    '18',
                    '-pix_fmt',
                    'yuv420p',
                    '-acodec',
                    'copy',
                    '-f',
                    'mp4',
                    'b']
        self._test_profile(profile_raw, expected)

    def test_cmdline_ffmpeg_webm_vp9(self):
        profile_raw = {
            'container': 'webm',
            'vcodec': 'vp9',
            'acodec': 'opus',
            'vp9_deadline': 'best'
        }
        expected = ['-y',
                    '-i',
                    'a',
                    '-vcodec',
                    'libvpx-vp9',
                    '-deadline',
                    'best',
                    '-pix_fmt',
                    'yuv420p',
                    '-acodec',
                    'libopus',
                    '-f',
                    'webm',
                    'b']
        self._test_profile(profile_raw, expected)

    def test_cmdline_ffmpeg_webm_vp8(self):
        profile_raw = {
            'container': 'webm',
            'vcodec': 'vp8',
            'acodec': 'vorbis',
            'vp8_quality': 'best'
        }
        expected = ['-y',
                    '-i',
                    'a',
                    '-vcodec',
                    'libvpx',
                    '-quality',
                    'best',
                    '-crf',
                    '10',
                    '-pix_fmt',
                    'yuv420p',
                    '-acodec',
                    'libvorbis',
                    '-f',
                    'webm',
                    'b']
        self._test_profile(profile_raw, expected)

    def _test_profile(self, profile, expected):
        metadata = VideoMetadata()
        profile = Profile('test', profile)
        result = profile.cmdline_ffmpeg('a', 'b', metadata)
        self.assertListEqual(expected, result)

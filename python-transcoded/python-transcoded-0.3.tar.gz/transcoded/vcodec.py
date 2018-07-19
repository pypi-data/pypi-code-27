class H264:
    def __init__(self, profile):
        self.preset = profile['h264_preset'] if 'h264_preset' in profile else 'medium'
        self.tune = profile['h264_tune'] if 'h264_tune' in profile else None
        self.profile = profile['h264_profile'] if 'h264_profile' in profile else ['main']
        self.crf = int(profile['h264_crf']) if 'h264_crf' in profile else None
        self.params = profile['h264_params'] if 'h264_params' in profile else None
        self.faststart = self._str2bool(profile['h264_faststart']) if 'h264_faststart' in profile else False
        self.yuv420p = self._str2bool(profile['h264_yuv420p']) if 'h264_yuv420p' in profile else True

    def _str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def cmdline_ffmpeg(self, metadata):
        result = ['-preset', self.preset]
        if self.tune:
            result.extend(['-tune', self.tune])
        if self.profile:
            result.extend(['-profile:v', self.profile[0]])
        if self.crf:
            result.extend(['-crf', str(self.crf)])
        if self.faststart:
            result.extend(['-movflags', '+faststart'])
        if self.yuv420p:
            result.extend(['-pix_fmt', 'yuv420p'])
        return result


class VP9:
    def __init__(self, profile):
        self.hdr = self._str2bool(profile['vp9_hdr']) if 'vp9_hdr' in profile else False
        self.deadline = profile['vp9_deadline'] if 'vp9_deadline' in profile else 'good'
        self.yuv420p = self._str2bool(profile['vp9_yuv420p']) if 'vp9_yuv420p' in profile else True
        self.crf = int(profile['vp9_crf']) if 'vp9_crf' in profile else None

    def _str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def cmdline_ffmpeg(self, metadata):
        result = []
        if self.deadline:
            result.extend(['-deadline', self.deadline])
        if self.crf:
            result.extend(['-crf', str(self.crf)])
        if self.yuv420p:
            result.extend(['-pix_fmt', 'yuv420p'])
        return result


class VP8:
    def __init__(self, profile):
        self.quality = profile['vp8_quality'] if 'vp8_quality' in profile else 'good'
        self.yuv420p = self._str2bool(profile['vp8_yuv420p']) if 'vp8_yuv420p' in profile else True
        self.crf = int(profile['vp8_crf']) if 'vp8_crf' in profile else 10

    def _str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def cmdline_ffmpeg(self, metadata):
        result = []
        if self.quality:
            result.extend(['-quality', self.quality])
        if self.crf:
            result.extend(['-crf', str(self.crf)])
        if self.yuv420p:
            result.extend(['-pix_fmt', 'yuv420p'])
        return result

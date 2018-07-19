from transcoded import codecmap
from transcoded.vcodec import H264, VP9, VP8
from transcoded.struct import VideoMetadata


class Profile:
    def __init__(self, name, raw):
        self.name = name
        self.container = raw['container'] if 'container' in raw else 'mkv'
        self.vcodec = raw['vcodec'].split(',') if 'vcodec' in raw else ['copy']
        self.acodec = raw['acodec'].split(',') if 'acodec' in raw else ['copy']
        self.vpolicy = raw['vpolicy'] if 'vpolicy' in raw else 'only-mismatch'
        self.apolicy = raw['apolicy'] if 'apolicy' in raw else 'only-mismatch'
        self.vbitrate = raw['vbitrate'] if 'vbitrate' in raw else None
        self.abitrate = raw['abitrate'] if 'abitrate' in raw else None
        self.vbitrate_max = raw['vbitrate_max'] if 'vbitrate_max' in raw else None
        self.abitrate_max = raw['abitrate_max'] if 'abitrate_max' in raw else None
        self.twopass = self._str2bool(raw['twopass']) if 'twopass' in raw else False

        self.vprofile = None
        if self.vcodec[0] == 'h264':
            self.vprofile = H264(raw)
        elif self.vcodec[0] == 'vp9':
            self.vprofile = VP9(raw)
        elif self.vcodec[0] == 'vp8':
            self.vprofile = VP8(raw)

    def _str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def __repr__(self):
        return '<Profile {} {} v:{} a:{}>'.format(self.name, self.container, self.vcodec[0], self.acodec[0])

    def _compare_bitrate(self, a, b):
        a = self._parse_bitrate(a)
        b = self._parse_bitrate(b)
        return a > b

    def _parse_bitrate(self, a):
        a = a.lower()
        if a.endswith('k'):
            a = float(a[:-1]) * 1024
        elif a.endswith('m'):
            a = float(a[:-1]) * 1024 * 1024
        else:
            a = float(a)
        return int(a)

    def cmdline_ffmpeg(self, input, output, metadata):
        """
        :param input: Input files
        :param output: Output file
        :param metadata: Result from a metadata probe on the inputs
        :type metadata: VideoMetadata
        :return:
        """
        vcodec = self.vcodec[0]
        if metadata.video.codec in self.vcodec:
            if self.vpolicy == 'only-mismatch':
                if self._compare_bitrate(metadata.video.bitrate, self.vbitrate_max):
                    vcodec = metadata.video.codec
                else:
                    vcodec = 'copy'
            elif self.vpolicy == 'always-transcode':
                vcodec = metadata.video.codec

        acodec = self.acodec[0]
        for astream in metadata.audio:
            if astream.codec in self.acodec:
                if self.apolicy == 'only-mismatch':
                    if self._compare_bitrate(astream.bitrate, self.abitrate_max):
                        acodec = astream.codec
                    else:
                        acodec = 'copy'
                elif self.apolicy == 'always-transcode':
                    acodec = astream.codec

        cmdline = ['-y', '-i', input]

        vcodec = codecmap.getByCodec(vcodec).ffmpeg_encoder
        acodec = codecmap.getByCodec(acodec).ffmpeg_encoder
        container = codecmap.getByCodec(self.container).ffmpeg_encoder

        cmdline.extend(['-vcodec', vcodec])
        if vcodec != 'copy' and self.vbitrate is not None:
            cmdline.extend(['-b:v', self.vbitrate])
        if vcodec != 'copy' and self.vprofile:
            cmdline.extend(self.vprofile.cmdline_ffmpeg(metadata))

        cmdline.extend(['-acodec', acodec])
        if acodec != 'copy' and self.abitrate is not None:
            cmdline.extend(['-b:a', self.abitrate])

        cmdline.extend(['-f', container, output])
        return cmdline

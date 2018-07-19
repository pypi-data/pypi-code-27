import requests

from transcoded.executor import execute_ffmpeg
from transcoded.log import logger
from transcoded.probe import probe_file


class TranscodingJob:
    def __init__(self):
        self.sources = []
        self.destination = None
        self.profile = None
        self.foreign_id = None
        self.user = None
        self.callback = None

    def run(self):
        logger.info('Starting new task from {} for {}'.format(self.user, self.sources[0]))
        probe = probe_file(self.sources[0])
        command = self.profile.cmdline_ffmpeg(self.sources[0], self.destination, probe)
        self._callback({
            'status': 'started',
        })
        for progress in execute_ffmpeg(command, probe):
            logger.info('Progress: {}%'.format(progress))
            self._callback({
                'status': 'running',
                'progress': progress
            })
        logger.info('Job completed')
        self._callback({
            'status': 'done',
        })

    def _callback(self, payload):
        if self.callback is not None:
            base = {
                'source': self.sources[0],
                'destination': self.destination,
            }
            base.update(payload)
            if self.foreign_id is not None:
                base['id'] = self.foreign_id

            try:
                requests.post(self.callback, json=base)
            except Exception as e:
                logger.error('Callback "{}" responded with error on job {}'.format(payload['status'], self.foreign_id))
                logger.error('URL: {}'.format(self.callback))
                logger.error(e)

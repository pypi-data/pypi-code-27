import gzip
import logging
import sys
import time

import boto3
from boto3 import Session
from botocore.exceptions import ClientError

from leosdk.aws.cfg import Cfg
from leosdk.aws.leo_stream import LeoStream
from leosdk.aws.payload import Payload

logger = logging.getLogger(__name__)


class Kinesis(LeoStream):
    max_record_size: int
    max_batch_size: int
    max_batch_records: int
    max_batch_age: int
    max_attempts: int
    compressed_records: [dict]

    def __init__(self, config: Cfg, bot_id: str, queue_name: str):
        self.stream_name = config.value('STREAM')
        if self.stream_name is None:
            raise AssertionError("Missing 'STREAM' field for the current environment in leo_config.py")
        self.bot_id = bot_id
        self.queue_name = queue_name

        self.client = Kinesis.__aws_session(config).client('kinesis')
        self.max_record_size = config.int_value_or_else('STREAM_MAX_RECORD_SIZE', 1024 * 900)
        self.max_batch_size = config.int_value_or_else('STREAM_MAX_BATCH_SIZE', 1024 * 900)
        self.max_batch_records = config.int_value_or_else('STREAM_MAX_BATCH_RECORDS', 1000)
        self.max_batch_age = config.int_value_or_else('STREAM_MAX_BATCH_AGE', 200)
        self.max_attempts = config.int_value_or_else('STREAM_MAX_UPLOAD_ATTEMPTS', 10)
        self.compressed_records = []
        self.send_time = round(time.time() * 1000)

    def write(self, payload: Payload):
        compressed_payload = self.compress_rec(payload)
        compressed_payload_size = sys.getsizeof(compressed_payload)

        if self.exceeds_payload_size(compressed_payload_size):
            raise ValueError("Payload size is larger than %d bytes" % self.max_record_size)

        if self.send_required(compressed_payload_size):
            self.send()
        self.append_record(compressed_payload)

    def end(self):
        self.send()
        logger.info('End Kinesis stream')

    def send(self):
        attempts = 0
        while len(self.compressed_records) > 0:
            result = self.send_current(attempts)
            attempts += 1
            if result.get('FailedRecordCount') == 0 or attempts >= self.max_attempts:
                self.log_successes()
                break
            else:
                self.log_failures(result)

        self.compressed_records.clear()
        self.send_time = round(time.time() * 1000)

    def send_current(self, attempts: int) -> {}:
        try:
            time.sleep(attempts * .1)
            return self.client.put_records(
                Records=self.compressed_records,
                StreamName=self.stream_name
            )
        except ClientError:
            return {'FailedRecordCount': len(self.compressed_records)}

    def send_required(self, size: int) -> bool:
        return self.exceeds_batch_size(size) or self.exceeds_batch_age() or self.exceeds_batch_records()

    def exceeds_payload_size(self, compressed_payload_size: int) -> bool:
        return compressed_payload_size > self.max_record_size

    def exceeds_batch_size(self, compressed_payload_size: int) -> bool:
        batch_size = sys.getsizeof(self.compressed_records)
        return batch_size + compressed_payload_size > self.max_batch_size

    def exceeds_batch_age(self) -> bool:
        now = round(time.time() * 1000)
        return now - self.send_time > self.max_batch_age

    def exceeds_batch_records(self) -> bool:
        return len(self.compressed_records) >= self.max_batch_records

    def append_record(self, compressed_payload: {}):
        self.compressed_records.append(compressed_payload)

    def log_successes(self):
        uploaded = len(self.compressed_records)
        batch_size = sys.getsizeof(self.compressed_records)
        plural = 's' if uploaded > 1 else ''
        logger.debug('Uploaded %d compressed payload%s to Kinesis with a total of %d bytes',
                     uploaded, plural, batch_size)

    def compress_rec(self, payload: Payload) -> {}:
        payload.set_id(self.bot_id)
        payload.set_event(self.queue_name)
        return {
            'Data': gzip.compress(bytes(payload.get_payload_data(), 'UTF-8')),
            'PartitionKey': payload.get_id()
        }

    @staticmethod
    def __aws_session(config: Cfg) -> Session:
        profile = config.value('AWS_PROFILE')
        region = config.value('REGION')
        return boto3.Session(profile_name=profile, region_name=region)

    @staticmethod
    def log_failures(result: {}):
        recs = result.get('Records')
        if not recs:
            return
        for i in recs:
            code = recs[i].get('ErrorCode')
            if code:
                seq = recs[i].get('SequenceNumber')
                msg = recs[i].get('ErrorMessage')
                logger.warning("Error %s sending record with sequence %s: %s" % (code, seq, msg))

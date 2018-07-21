import os
import time
import boto3
import fnmatch
import subprocess
import logging
import argparse
from threading import Thread
from queue import Queue

logging.Formatter.converter = time.gmtime
logging.basicConfig(format='%(asctime)s::%(name)s::%(levelname)s::%(message)s')
logger = logging.getLogger('s3-to-disk')
logger.setLevel(logging.INFO)


def run_threads(routine, n=1):
    threads = []
    for i in range(n):
        t = Thread(target=routine, args=(i,))
        t.daemon = True
        t.start()
        threads.append(t)
    return threads


class S3ToDisk(object):
    def __init__(self, data_dir, log_dir, glob='*', dry_run=False, timeout=0, worker_count=1):
        self.data_dir = data_dir
        self.log_dir = log_dir
        self.dry_run = dry_run
        self.glob = glob
        self.worker_count = worker_count
        self.queue = Queue()
        self.children_procs = []
        self.timeout = timeout
        self._lock = '/tmp/.s3_to_disk_{}.lock'.format(abs(hash(tuple([self.data_dir, self.log_dir]))))

    def sync(self):
        self.lock()
        try:
            self._sync()
        except Exception:
            raise
        finally:
            self.unlock()

    def _sync(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        logger.info('begin')

        s3 = boto3.resource('s3')
        buckets = [b.name for b in s3.buckets.all() if fnmatch.fnmatch(b.name, self.glob)]
        logger.info('count={}'.format(len(buckets)))
        for bucket in buckets:
            self.queue.put(bucket)
            logger.info('added::{}'.format(bucket))

        workers = run_threads(self._sync_worker, self.worker_count)
        if self.timeout > 0:
            run_threads(self._interrupt_execution_worker)
        self.queue.join()
        [t.join() for t in workers]

        logger.info('end')

    def sync_bucket(self, bucket_name):
        prefix = 'sync-bucket::{}::'.format(bucket_name)
        logger.info(prefix + 'begin')

        bucket_dir = os.path.join(self.data_dir, bucket_name)
        if not os.path.exists(bucket_dir):
            os.makedirs(bucket_dir)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_path = os.path.join(self.log_dir, '{}.log'.format(bucket_name))
        cmd = ['aws', 's3', 'sync', 's3://{}'.format(bucket_name), bucket_dir, '--region', 'eu-west-1']
        if self.dry_run:
            cmd.append('--dryrun')
        logger.info(prefix + 'cmd::{}'.format(' '.join(cmd)))
        with open(log_path, 'w') as f:
            logger.info(prefix + 'logs::tail -f {}'.format(log_path))
            proc = subprocess.Popen(cmd, stdout=f)
            logger.info(prefix + 'subprocess::pid={}::begin'.format(proc.pid))
            self.children_procs.append(proc)
            if proc.wait() == 0:
                logger.info(prefix + 'subprocess::pid={}::end'.format(proc.pid))
            else:
                logger.info(prefix + 'subprocess::pid={}::terminated'.format(proc.pid))
            self.children_procs.remove(proc)
        logger.info(prefix + 'end')

    def _interrupt_execution_worker(self, n):
        """ Interrupts a sync job after a given timeout in seconds.

        This is usefull because of an underlying haning problem in the awscli.
        """
        time.sleep(self.timeout)
        logger.info('interrupt-execution::begin')
        # emtpy queue
        while not self.queue.empty():
            self.queue.get()
            self.queue.task_done()
        [p.kill() for p in self.children_procs]
        logger.info('interrupt-execution::end')

    def _sync_worker(self, n):
        """A thread that will execute sync commands.
        """
        prefix = 'worker-{}::'.format(n)
        logger.debug(prefix + 'joined')
        while not self.queue.empty():
            bucket = self.queue.get()
            logger.debug(prefix + 'run::{}::begin'.format(bucket))
            self.sync_bucket(bucket)
            self.queue.task_done()
            logger.debug(prefix + 'run::{}::end'.format(bucket))
        logger.debug(prefix + 'left')

    def lock(self):
        if not os.path.exists(self._lock):
            open(self._lock, 'a').close()
        else:
            msg = [
                'Make sure another instance of this process is not running.',
                'You can make this message disappear by deleting {} file'.format(self._lock)]
            print('\r\n'.join(msg))
            exit()

    def unlock(self):
        if os.path.exists(self._lock):
            os.remove(self._lock)


def main():
    parser = argparse.ArgumentParser('s3-to-disk')
    parser.add_argument('-D', '--data-dir', required=True)
    parser.add_argument('-L', '--log-dir', default='log')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('-g', '--glob', default='*')
    parser.add_argument('-c', '--worker-count', type=int, default=1)
    parser.add_argument('-t', '--timeout-in-seconds', type=int, default=0)
    args = parser.parse_args()

    s = S3ToDisk(
        args.data_dir,
        args.log_dir,
        glob=args.glob,
        dry_run=args.dry_run,
        worker_count=args.worker_count,
        timeout=args.timeout_in_seconds)
    s.sync()


if __name__ == '__main__':
    main()

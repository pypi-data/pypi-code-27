import os
import sys
import logging

logger = logging.getLogger(os.path.basename(sys.argv[0]))


class Source(object):

    def __init__(self, work_dir=None, backup=False,
                 cleanup=True, dry_run=False):
        self.work_dir = work_dir
        self.backup = backup
        self.cleanup = cleanup
        self.dry_run = dry_run
        self.working_files = []

    def get(self):
        file_list = self.__get_file_list()
        self.working_files = self.__fetch(file_list)
        if self.backup:
            self.__backup(file_list)
        else:
            logger.warning("src backup disabled")
        if self.cleanup:
            self.__cleanup(file_list)
        else:
            logger.warning("src cleanup disabled")
        return self.working_files

    def __get_file_list(self):
        logger.warning("getting file list")
        return self.get_file_list()

    def __fetch(self, file_list):
        logger.warning("fetching from src")
        return self.do_fetch(file_list)

    def __backup(self, file_list):
        logger.warning("creating src backup")
        self.do_backup(file_list)

    def __cleanup(self, file_list):
        logger.warning("cleaning up src")
        self.do_cleanup(file_list)

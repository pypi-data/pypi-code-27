import os
import sys
import glob
import errno
import shutil
import datetime

from . import Source, logger


class FileSource(Source):

    def __init__(self, work_dir=None, backup=True,
                 cleanup=True, dry_run=False, path=None):
        Source.__init__(self, work_dir, backup, cleanup, dry_run)
        self.path = path

    def get_file_list(self):
        files = glob.glob(self.path)
        logger.info("found %d files matching path %s" % (len(files), self.path))
        if len(files) < 1:
            logger.warning("no files found for processing")
            sys.exit()
        return files

    def do_fetch(self, file_list):
        working_file_list = []
        for f in file_list:
            file_basename = os.path.basename(f)
            working_file = os.path.join(self.work_dir, file_basename)
            working_file_list.append(working_file)
            if self.dry_run:
                logger.info("would have copied %s to %s" % (f, working_file))
            else:
                logger.info("copying %s to %s" % (f, working_file))
                shutil.copyfile(f, working_file)
        return working_file_list

    def do_backup(self, file_list):
        src_dir = os.path.dirname(file_list[0])
        now = datetime.datetime.now()
        backup_dir = os.path.join(src_dir,
                                  "backup",
                                  '%d' % now.year,
                                  '%02d' % now.month,
                                  '%02d' % now.day)
        try:
            if self.dry_run:
                logger.info("would have created backup directory %s" % backup_dir)

            else:
                if not os.path.isdir(backup_dir):
                    logger.warning("creating backup directory %s" % backup_dir)
                    try:
                        os.makedirs(backup_dir)
                    except OSError as e:
                        if e.errno != errno.EEXIST:
                            raise

            for f in file_list:
                file_basename = os.path.basename(f)
                backup_file = os.path.join(backup_dir, file_basename)
                if self.dry_run:
                    logger.info("would have created backup copy of %s as %s" % (
                            f,
                            backup_file
                        ))
                else:
                    logger.info("creating backup of %s at %s" % (
                            f,
                            backup_file
                        ))
                    shutil.copyfile(f, backup_file)

        except (IOError, OSError):
            logger.critical(
                "permission denied whilst creating backup directory %s"
                % backup_dir)
            sys.exit(1)

    def do_cleanup(self, file_list):
        for f in file_list:
            if self.dry_run:
                logger.info("would have cleaned up %s" % f)
            else:
                logger.info("cleaning up %s" % f)
                try:
                    os.remove(f)
                except (IOError, OSError) as e:
                    logger.error("%s %s" % (e.strerror, e.filename))

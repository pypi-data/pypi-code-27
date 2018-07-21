import os, sys, logging
import aperture.util.files as utl_f

COLORS = {
    'INFO': '\u001b[0m',
    'EXTRAINFO': '\u001b[0m',
    'SUCC': '\u001b[32m',
    'WARN': '\u001b[33m',
    'ERROR': '\u001b[31m',
    '.jpg': '\u001b[38;5;81m',
    '.gif': '\u001b[38;5;229m',
    '.png': '\u001b[38;5;198m'
}

widths = (40, 40, 10)


class ApertureLogger(object):

    def __init__(self):
        '''Constructor'''
        self.__verbose = False
        self.__log_file = None

    '''Getters and Setters'''

    @property
    def log_file(self):
        return self.__log_file

    @log_file.setter
    def log_file(self, f):
        self.__log_file = f
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, v):
        self.__verbose = v

    '''Class methods'''

    def log(self, message, level):
        '''Print out a message to the console.

        Args:
            message: A string containing the message to be printed.
            level: A string containing the level of the message.
        '''

        level = level.upper()

        if self.verbose or level == 'ERROR' or level == 'SUCC' or level == 'EXTRAINFO':
            output = ''

            # If the os is windows ignore coloring
            if not os.name == 'nt':
                output += COLORS[level]

            print(output + message)

            # Set the color to white after
            if not os.name == 'nt':
                sys.stdout.write(COLORS['INFO'])

        if self.log_file is not None:
            logger = logging.getLogger()
            if level == 'INFO' or level == 'SUCC' or level == 'EXTRAINFO':
                logger.info(message)
            elif level == 'WARN':
                logger.warning(message)
            elif level == 'ERROR':
                logger.error(message)


def display_verbose_table(files):
    '''Displays the verbose output table for all processed image.

        Displays the file size comparison of the original an new image.

        Args:
            files: A dictionary containing tuples of filenames and filesizes for various resolutions.
        '''

    print('\n\t{} | {} | {}'.format('original'.ljust(widths[0]), 'result'.ljust(
        widths[1]), 'savings'.ljust(widths[2])))
    print('\t{}'.format('-' * (sum(widths) + 6)))

    image_count = len(files['orig'])
    extra_line = len(files) > 2

    for image_index in range(image_count):
        orig_line = True
        orig = files['orig'][image_index]
        line = '\t{} | '.format(get_table_filename(orig, True).ljust(widths[0]))

        for output_index in range(1, len(files)):
            current = files[list(files)[output_index]][image_index]

            if orig_line:
                line += '{} | {}'.format(
                    get_table_filename(current).ljust(widths[1]),
                    utl_f.bytes_to_readable(orig[1] - current[1]).rjust(10))
                orig_line = False
            else:
                line = '\t{} | {} | {}'.format(
                    ' ' * widths[0],
                    get_table_filename(current).ljust(widths[1]),
                    utl_f.bytes_to_readable(orig[1] - current[1]).rjust(10))

            print(line)

        if extra_line and not image_index == image_count - 1:
            print('\t{} | {} |'.format(' ' * widths[0], ' ' * widths[1]))

    print('\n')


def get_table_filename(file_tuple, color_ext=False):
    '''Creates a filename entry for the vebose output table with truncation if necessary.

    Args:
        file_tuple: A tuple containing the file's name and size.
        color_ext: A boolean whether the file's extension should be colored.

    '''
    filename = os.path.split(file_tuple[0])[1]
    filesize = '[{}]'.format(utl_f.bytes_to_readable(file_tuple[1]))

    filename_space = widths[0] - len(filesize)

    fn, ext = os.path.splitext(filename)
    if len(filename) < filename_space:
        space_count = filename_space - len(filename)
        trunc_name = fn
    else:
        # Compress filename with an elipses
        space_count = 1
        trunc_name = '{}...{}'.format(
            fn[:filename_space - len(ext) - len(fn) - 21], fn[len(fn) - 17:])

    if color_ext and not os.name == 'nt':
        temp_ext = ext.lower()
        if temp_ext == '.jpeg':
            temp_ext = '.jpg'
        new_ext = '{}{}{}'.format(COLORS[temp_ext], ext, COLORS['INFO'])
        ext = new_ext

    return '{}{}{}{}'.format(trunc_name, ext, ' ' * space_count, filesize)


apt_logger = ApertureLogger()

import os

import aperture.util.files as utl_f
import aperture.util.directories as utl_d
import aperture.errors as errors
import aperture.config_file as cfg_f
from aperture.util.output import apt_logger as logger
from aperturelib import SUPPORTED_EXTENSIONS

DEFAULT_QUALITY = 75
QUALITY_MIN = 1
QUALITY_MAX = 95
DEFAULT_DIR = os.getcwd()
GIF_WARN = False


def deserialize_options(options, config_dict):
    '''Deserialize and parse each of the provided options.

    Args:
        options: A dictionary with each command-line option and their values.
        config_dict: A dictionary with options extracted from a config file.

    Returns:
        A dictionary with parsed values for each option.
    '''
    deserialized = {}

    # Option value precedence:
    # 1. CMD-line arguments
    # 2. Config file options
    inputs = options['<input>']
    outpath = cfg_f.config_or_provided('outpath', config_dict, options)
    quality = cfg_f.config_or_provided('quality', config_dict, options)
    resolutions = cfg_f.config_or_provided('resolutions', config_dict, options)
    verbose = cfg_f.config_or_provided('verbose', config_dict, options)
    depth = cfg_f.config_or_provided('max-depth', config_dict, options)
    log = cfg_f.config_or_provided('log', config_dict, options)
    watermark_image = cfg_f.config_or_provided('wmark-img', config_dict,
                                               options)
    watermark_text = cfg_f.config_or_provided('wmark-txt', config_dict, options)

    # Parse and extract the values from the options to be sent into aperture.
    deserialized['verbose'] = verbose
    deserialized['log'] = log
    logger.verbose = verbose
    if log:
        logger.log_file = '{}{}{}'.format(os.getcwd(), os.sep, '.aperture.log')
    deserialized['max-depth'] = parse_recursion_depth(depth)
    deserialized['inputs'] = parse_inputs(inputs, deserialized['max-depth'])
    deserialized['output'] = parse_outpath(outpath)
    deserialized['quality'] = parse_quality(quality)
    deserialized['resolutions'] = parse_resolutions(resolutions)
    deserialized['wmark-img'] = parse_watermark_image(watermark_image)
    # Dont really need to parse watermark text because it's either words or it's nothing
    deserialized['wmark-txt'] = watermark_text

    return deserialized


def parse_outpath(outpath):
    '''Parse and extract the output path for the processed images.

    Creates the necessary directories for the output path if it does not exist.

    Args:
        outpath: A string containing the desired output path.

    Returns:
        A string containing the final output path.

    Raises:
        ApertureError: An error occured when creating any necessary directories.
    '''
    if outpath is None:
        outpath = DEFAULT_DIR
        logger.log('No outpath provided, using the current working directory.',
                   'info')
    elif outpath == '.':
        # repetion here so we can have the above warning log
        outpath = DEFAULT_DIR
    else:
        outpath = os.path.expanduser(outpath)
        if not os.path.isdir(outpath):  # make the directory or directories
            try:
                utl_d.make_necessary_directories(outpath)
            except PermissionError as e:
                raise errors.ApertureError(
                    'Permission denied: \'{}\''.format(outpath))
            except OSError as e:  # catch-all
                raise errors.ApertureError(
                    'Failed to create directory \'{}\'.'.format(outpath))

    return outpath


def parse_recursion_depth(depth):
    '''Parse and validate the maximum recursion depth for directory traversal

    Args:
        depth: An integer containing the maximum recursion depth.

    Returns:
        An integer containing the parsed maximum recursion depth.

    Raises:
        ApertureError: An error occured when parsing the maximum recursion depth.
    '''

    err = 'Supplied depth value \'{}\' is not valid. Depth value must be an integer and be greater than 0.'.format(
        depth)

    try:
        depth = int(depth)
    except ValueError:
        raise errors.ApertureError(err)

    if depth < 0:
        raise errors.ApertureError(err)

    return depth


def parse_inputs(inputs, depth):
    '''Parse and extract the input paths.

    Traverses directories to find all compatible image file paths.
    A path can also just be an explicit image path, instead of a directory.

    Args:
        inputs: A list of inputs containing either directories, explicit file paths or both.

    Returns:
        A list of file paths based on the provided input paths.

    Raises:
        ApertureError: An error occured when parsing the input paths.
    '''
    global GIF_WARN
    GIF_WARN = False
    file_paths = []
    inputs = [DEFAULT_DIR] if inputs is None or inputs == '.' else inputs
    for path in inputs:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            try:
                #Gets all files (and only files) from supplied path and subdirectories recursively up to a given depth
                files = utl_f.get_files_in_directory_recursive(
                    path, max_depth=depth)
            except FileNotFoundError:
                raise errors.ApertureError(
                    'Could not locate directory \'{}\''.format(path))
            except PermissionError as e:  # Directory has no read access
                raise errors.ApertureError(
                    'Permission denied: \'{}\''.format(path))
            for current_file in files:
                if is_compatible_file(current_file, SUPPORTED_EXTENSIONS):
                    file_paths.append(current_file)
                else:
                    logger.log(
                        'File \'{}\' is not a supported image file.'.format(
                            current_file), 'warn')

        elif os.path.isfile(path):
            if is_compatible_file(path, SUPPORTED_EXTENSIONS):
                file_paths.append(path)
            else:
                logger.log(
                    'File \'{}\' is not a supported image file.'.format(path),
                    'warn')
        else:
            logger.log('Could not locate input \'{}\'.'.format(path), 'warn')

    if len(file_paths) == 0:
        raise errors.ApertureError('No valid input files found')

    return file_paths


def parse_quality(quality):
    '''Parses and validate the quality value.
    
    Args:
        quality: A integer containing the quality value
    
    Returns:
        An integer containing the parsed quality value
    
    Raises:
        ApertureError: An error occured parsing the quality value.
    '''
    err = 'Supplied quality value \'{}\' is not valid. Quality value must be between 1 and 95'.format(
        quality)

    try:
        quality = int(quality)
    except ValueError:
        raise errors.ApertureError(err)

    if quality not in range(QUALITY_MIN, QUALITY_MAX + 1):
        raise errors.ApertureError(err)

    return quality


def parse_resolutions(resolutions):
    '''Parses and extracts the resolutions to use for resizing each image.

    Args:
        resolutions: A string containing image resolutions.
            The resolution string is expected to have an 'x' used to separate
            the dimensions of each resolution.
            If multiple resolutions are provided, they must be wrapped in a string
            with each resolution separated by a space.
            
            Examples:
            800x800
            "1600x900 1280x1024"

    Returns:
        A list of tuples for each resolution, where each tuple is (width, height).

    Raises:
        ApertureError: An error occurred parsing the resolutions.
    '''
    resolutions_parsed = []
    if resolutions is not None:
        resolutions = resolutions.split(' ')
        for res in resolutions:
            try:
                w, h = res.lower().split('x')
                r = (int(w), int(h))
            except ValueError:
                raise errors.ApertureError(
                    'Supplied resolution \'{}\' is not valid. Resolutions must be in form \'<width>x<height>\''.
                    format(res))
            else:
                resolutions_parsed.append(r)

    return resolutions_parsed


def parse_watermark_image(watermark_path):
    '''Parses and extracts the path to the watermark image to use.

    Args:
        watermark_path: A string to the desired watermark image to use.

    Returns:
        The path to the watermark image if the provided image existed and
        was a valid size and format.

    Raises:
        ApertureError: An error occurred parsing the watermark image path.
    '''
    if not watermark_path:
        return None
    else:
        watermark_path = os.path.expanduser(watermark_path)
        if not os.path.isfile(watermark_path):
            raise errors.ApertureError(
                'Supplied path \'{}\' does not exist.'.format(watermark_path))
        else:
            if is_compatible_file(watermark_path, SUPPORTED_EXTENSIONS):
                #watermark_image = Image.open(watermark_path)
                return watermark_path
            else:
                raise errors.ApertureError(
                    'File \'{}\' is not a supported image file.'.format(
                        watermark_path))


# TODO: Ignore hidden files (i.e. .DS_Store, .gitignore)
def is_compatible_file(path, extensions):
    '''Determines if a file path is a compatible image file.

    Args:
        path: A string containing a path to the file.
        extension: A list of supported extensions to validate the file against.
    
    Returns:
        A boolean indicating whether or not the file is a compatible image file.
    '''
    ext = os.path.splitext(path)[1].lower()
    global GIF_WARN
    if not GIF_WARN:
        warn_gif(path, ext)

    return ext in extensions


def warn_gif(path, ext):
    '''Warns user that animated GIF's are not supported.

    Args:
        path: A string containing a path to the file.
        ext: File extension of the provided path.
    '''
    if ext == '.gif':
        logger.log(
            'GIF file(s) entered as input: Aperture does not support animated GIF\'s. Animated GIF\'s will only have their first frame saved.',
            'warn')
        global GIF_WARN
        GIF_WARN = True

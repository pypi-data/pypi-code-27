import os
import ntpath
import shutil
import aperturelib as apt
import aperture.util.files as utl_f
from .command import Command
import aperture.util.output as utl_o
from aperture.util.output import apt_logger as logger


class Aperture(Command):

    def run(self):
        '''Runs the 'aperture' command.'''

        options = self.options

        inputs = options['inputs']
        out_path = options['output']
        quality = options['quality']
        verbose = options['verbose']

        # Dictionary required for success output
        res_keys = options['resolutions'].copy()
        files = {'orig': []}
        if res_keys == []:
            res_keys.append('new')
            files['new'] = []
        else:
            for res in res_keys:
                files[res] = []

        # lambda function to return filename and size as a tuple
        # where f is a file name
        filename_size = lambda f: (f, os.path.getsize(f))

        for image_path in inputs:
            results = apt.format_image(image_path, options)

            # Record the original size of the image once
            flnmsz_in = filename_size(image_path)
            files['orig'].append(flnmsz_in)

            for index in range(len(results)):
                image = results[index]

                # Get the output file path
                out_file = get_image_out_path(image, image_path, out_path,
                                              options)

                # Save the image, apply quality LAST
                pil_opts = {'quality': quality}

                # Use this instead of image.format b/c after resizing/watermarking
                #  image.format is usually None
                img_format = os.path.splitext(image_path)[1].upper()[1:]

                #Make sure we at least try to compress all files types
                if img_format in ['JPG', 'JPEG']:
                    if quality <= 60:
                        pil_opts['optimize'] = True
                elif img_format == 'PNG' and image.mode not in ['P', 'L']:
                    '''
                    'quality' values from 1-95 will map to compress_level values between 1 and 9. 
                    all values of 'quality' below 47 will map to maximum compression (9). This is because
                    this compression doesn't actually degrade image quality, even though the quality
                    attribute for .jpg images does. Because of this, users are more likely to provide 
                    higher quality levels than lower ones, but we still want them to get a good level 
                    of compression with their .png images.
                    ---------------------------
                    0-46    = 9     71-76   = 4
                    47-52   = 8     77-82   = 3
                    53-58   = 7     83-88   = 2
                    59-64   = 6     89-95   = 1
                    65-70   = 5
                    ---------------------------
                    '''
                    comp_lvl = 10 - int((((quality + 5) - 40) / 6))
                    if comp_lvl == 0:
                        comp_lvl = 1
                    elif comp_lvl > 9:
                        comp_lvl = 9
                    pil_opts['compress_level'] = comp_lvl
                    #If input image was PNG and desired quality was <=20, convert to palette image
                    if quality <= 20:
                        #Degrades image quality but decreases file size dramatically
                        image = image.convert('P', palette=1, colors=256)
                elif img_format in ['PNG', 'GIF']:
                    # NOTE:
                    # Only single frame Gif's will be handled. Animated Gif's will only have
                    #  their first frame saved

                    # TODO:
                    #Single frame gif's can be compressed a lot if converted to jpg... maybe we can ask
                    # users if they want to allow gifs to be converted for more compression?
                    #if img_format == 'GIF':
                    #   image = image.convert('RGB')
                    #   out_file = out_file[:-4] + '.jpg'
                    '''
                    Not sure why this works, but converting palette images to RGB
                    and then back to palette helps compress them much better than
                    just trying to save the palette image
                    '''
                    was_P = image.mode == 'P'
                    was_L = image.mode == 'L'

                    #Size of original palette
                    if was_P:
                        cols = int(len(image.getpalette()) / 3)

                    if image.mode not in ['RGB', 'RGBA']:
                        image = image.convert('RGBA')

                    if was_P:
                        image = image.convert('P', palette=1, colors=cols)
                    elif was_L:
                        image = image.convert('L')

                    #.gif images are always 'P' or 'L' mode.
                    #For palette images, just compress as much as possible always
                    pil_opts['optimize'] = True

                apt.save(image, out_file, **pil_opts)

                #If file was not modified except for attempted compression and
                # output file is larger than input file, replace output file with
                # input file.
                flnmsz_out = filename_size(out_file)
                if (not options['wmark-txt']) and (
                        not options['wmark-img']) and (
                            not options['resolutions']):
                    if flnmsz_out[1] > flnmsz_in[1]:
                        shutil.copy(image_path, out_file)
                        flnmsz_out = filename_size(out_file)

                # For each resolution (if no resolution specified do once with key 'new')
                # record the resulting file size
                files[res_keys[index]].append(flnmsz_out)

                # Print the results of the pipeline
                logger.log('File \'{}\' created.'.format(out_file), 'info')

        # Print savings table if verbose
        if logger.verbose:
            utl_o.display_verbose_table(files)

        # Sum the image sizes for each element within the sizes
        sizes = {}
        for key in files:
            sizes[key] = sum(list(map(lambda x: x[1], files[key])))

        # Determine the savings for each specified resolution
        # (or once if no resolutions provided)

        image_count_str = 'Input images: {}\nOutput images: {}'
        if res_keys == ['new']:
            logger.log(
                image_count_str.format(len(inputs), len(inputs)), 'extrainfo')
            logger.log(
                'Total savings: {}'.format(
                    utl_f.bytes_to_readable(sizes['orig'] - sizes['new'])),
                'succ')
        else:
            logger.log(
                image_count_str.format(
                    len(inputs),
                    len(inputs) * (len(sizes) - 1)), 'extrainfo')
            for i in range(1, len(sizes)):
                res = res_keys[i - 1]
                res_str = '{}x{}'.format(res[0], res[1])
                logger.log(
                    'Total savings for resolution {}: {}'.format(
                        res_str,
                        utl_f.bytes_to_readable(sizes['orig'] -
                                                sizes[list(sizes)[i]])), 'succ')


def get_image_out_path(image, orig_path, out_path, options):
    '''Gets the output path for an image.

    Extracts an apporpriate name for the image file based on
    the provided options. This file name is then included in
    the output path for the image.

    Args:
        image: An instance of a PIL image.
        orig_path: The path to the original image.
        out_path: The path to the output directory.
        options: A dictionary of options from the command class instance.

    Returns:
        A string containing the complete output path for the image.
    '''
    filename, extension = os.path.splitext(ntpath.split(orig_path)[1])
    added_text = ''

    # Assume that if resolutions existed, resizing occurred.
    if options['resolutions']:
        # Include resized resolution into file name for now.
        size = image.size
        added_text += '_' + str(size[0]) + '_' + str(size[1]) + '_'

    # TODO: Replace with a "--postfix" option or something from cmd args.
    added_text += 'cmprsd'

    out_file = os.path.join(out_path, filename + added_text + extension)

    return out_file

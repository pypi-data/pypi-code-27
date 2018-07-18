# -*- coding: utf-8 -*-
"""
Module containing the functions for transforming all the files contained
in a directory and interacting with the user through the command line.
"""

import os
from os import path as osp
import json
import shutil
import stat
import sys
import gc
from tempfile import mkstemp
import multiprocessing as mp
import logging

from glamconv.transformer.processes import Process
from glamconv import ead

_ACTIONS_REGISTERED = False


def register_actions():
    global _ACTIONS_REGISTERED
    if not _ACTIONS_REGISTERED:
        ead.register()
        _ACTIONS_REGISTERED = True


def build_progress_function(process):
    step_names = [step.action.name for step in process.steps]

    def progress(starting_step_index):
        sys.stdout.write(u"\r\033[K")
        sys.stdout.write(u"    running step: {0} ({1:d}/{2:d})"
                         u"".format(step_names[starting_step_index],
                                    starting_step_index + 1, len(step_names)))
        sys.stdout.flush()
    return progress


def batch_ead2_to_ape(arglist, processes=mp.cpu_count()):
    """convenience entry point to run ead2_to_ape on a list of XML files

    Parameters
    ----------
    arglist: a list of tuple of arguments to be passed to ``ead2_to_ape``,
             (e.g. [('/tmp/input1.xml', '/tmp/output1.xml'),
                    ('tmp/input2.xml', '/tmp/output2.xml')])
    processes: the number of CPU to dispatch the batch on
    """
    pool = mp.Pool(processes=processes)
    pool.map(_convert_to_ape, arglist)


def _convert_to_ape(inputargs):
    try:
        ead2_to_ape(*inputargs)
    except Exception:
        logger = logging.getLogger('glamconv.ead')
        logger.exception('failed to convert_to_ape', inputargs[0])


def ead2_to_ape(input_filepath_or_tree, output_filepath, settings=None):
    """

    Parameters
    -----------

    - `input_filepath_or_tree`: path to the input file or an already parsed
      lxml tree
    - `output_filepath`: path to the output file
    - `settings`: dictionary defining the transformation process (list
      of steps and options).
    """
    if settings is None:
        settings = ead.ead2_to_ape_default_settings()
    register_actions()
    logger = logging.getLogger(settings.get('logger', 'glamconv.ead'))
    if hasattr(input_filepath_or_tree, 'findtext'):
        identifier = input_filepath_or_tree.findtext('eadheader/eadid')
    else:
        identifier = osp.basename(input_filepath_or_tree)
    transform_input = input_filepath_or_tree
    logger.debug('processing %s', identifier)
    transform = Process('ead-2002', 'ape-ead', settings['steps'])
    # Collect files to process
    sys.stdout.write(u"Collecting files to process\n")
    output_dir = osp.dirname(output_filepath)
    if not osp.isdir(output_dir):
        os.makedirs(output_dir)
    if hasattr(input_filepath_or_tree, 'findtext'):
        logger.debug('processing %s',
                     input_filepath_or_tree.findtext('eadheader/eadid'))
    else:
        logger.debug('processing %s', osp.basename(input_filepath_or_tree))
    # Change steps parameters if asked to
# XXX    if adapt_process_params is not None:
# XXX        adapt_process_params(prc, norm_fname)
    # Actual transformation
    temp_fdesc, temp_fname = mkstemp(suffix=transform.output_format.file_ext)
    try:
        with open(temp_fname, "w") as out_stream:
            log = transform.run(transform_input, out_stream)
        os.close(temp_fdesc)
        # Just to be sure, we do what we can to clean the XML tree
        gc.collect()
        if osp.getsize(temp_fname) > 0:
            shutil.copy(temp_fname, output_filepath)
            os.chmod(output_filepath, (stat.S_IRUSR | stat.S_IWUSR |
                                       stat.S_IRGRP | stat.S_IWGRP |
                                       stat.S_IROTH))
        else:
            log.warning(
                "transformation of %s didn't generate any output",
                transform_input
            )
    finally:
        if osp.isfile(temp_fname):
            os.remove(temp_fname)
    # Log file
    log_fname = osp.join(
        output_dir,
        u"{0}.log.json".format(osp.splitext(osp.basename(output_filepath))[0])
    )
    with open(log_fname, u"w") as log_stream:
        json.dump(log.dump(), log_stream)


def transform_files_from_dir(process_filename, input_dir, output_dir,
                             recursive=True, adapt_process_params=None):
    # Build process
    sys.stdout.write(u"Building transformation process\n")
    with open(process_filename) as inp:
        prc = Process.from_json(json.load(inp))
    prg_func = build_progress_function(prc)
    inp_ext = prc.input_format.file_ext
    out_ext = prc.output_format.file_ext
    # Collect files to process
    sys.stdout.write(u"Collecting files to process\n")
    files_to_process = []
    if recursive:
        files_iter = os.walk(input_dir, followlinks=True)
    else:
        files_iter = [(input_dir, [], fname)
                      for fname in os.listdir(input_dir)]
    for dirname, subdirs, files in files_iter:
        out_dirname = osp.join(output_dir, osp.relpath(dirname, input_dir))
        # Normalize output dirname
        norm_out_dirname = out_dirname.decode(u"ascii", u"replace")
        norm_out_dirname = norm_out_dirname.replace(u"\ufffd", u"X")
        norm_out_dirname = norm_out_dirname.replace(u" ", u"_")
        # Create output structure
        if not osp.isdir(norm_out_dirname):
            os.makedirs(norm_out_dirname)
        for fname in files:
            if osp.splitext(fname)[1] not in (inp_ext, inp_ext.upper()):
                continue
            # Normalize filename
            norm_fname = fname.decode(u"ascii", u"replace")
            norm_fname = norm_fname.replace(u"\ufffd", u"X")
            norm_fname = norm_fname.replace(u" ", u"_")
            files_to_process.append(
                (norm_fname, dirname, fname, norm_out_dirname))
    files_number = len(files_to_process)
    sys.stdout.write(u"    found {0:d} files to process\n\n"
                     u"".format(files_number))
    # Run transformation
    abstract = {u"OK": [], u"OK-invalid-input": 0, u"INVALID": [],
                u"FAILED": [], u"ERROR": []}
    for file_idx, (norm_fname, inp_dirname, inp_filename, out_dirname) in \
                                                enumerate(files_to_process):  # noqa
        sys.stdout.write(u"*** {0} ({1:d}/{2:d})\n"
                         u"".format(norm_fname, file_idx, files_number))
        inp_fname = osp.join(inp_dirname, inp_filename)
        # Change steps parameters if asked to
        if adapt_process_params is not None:
            adapt_process_params(prc, norm_fname)
        # Actual transformation
        temp_fdesc, temp_fname = mkstemp(suffix=out_ext)
        with open(temp_fname, "w") as out_stream:
            with open(inp_fname) as inp_stream:
                log = prc.run(inp_stream, out_stream, prg_func)
        os.close(temp_fdesc)
        sys.stdout.write(u"\r\033[K")
        sys.stdout.flush()
        # Just to be sure, we do what we can to clean the XML tree
        gc.collect()
        # Choose output file and copy it in output dir
        fname_name, inp_ext = osp.splitext(norm_fname)
        out_fname = osp.join(out_dirname, fname_name)
        if log.output_validation:
            # Result is valid
            abstract[u"OK"].append(norm_fname)
            out_fname += out_ext
            msg = u"    OK"
            if not log.input_validation:
                msg += u" even if the input file was not valid"
                abstract[u"OK-invalid-input"] += 1
        elif log.failure:
            # An exception occured
            abstract[u"ERROR"].append(
                u"{0} (in step #{1:d})".format(norm_fname,
                                               (log.failure_step_index + 1)))
            out_fname += u".ERROR{0}".format(out_ext)
            msg = (u"    ERROR during transformation\n{0}"
                   u"".format(log.failure_message))
        elif log.input_validation:
            # Result is not valid and input was valid
            abstract[u"FAILED"].append(norm_fname)
            out_fname += u".FAILED{0}".format(out_ext)
            msg = (u"    FAILED\n{0}"
                   u"".format(log.output_validation_message))
        else:
            # Result is not valid but input wasn't valid
            abstract[u"INVALID"].append(norm_fname)
            out_fname += u".INVALID{0}".format(out_ext)
            msg = (u"    INVALID input\n{0}\n    INVALID output\n{1}"
                   u"".format(log.input_validation_message,
                              log.output_validation_message))
        sys.stdout.write(u"{0}\n".format(msg))
        if osp.getsize(temp_fname) > 0:
            shutil.copy(temp_fname, out_fname)
            os.chmod(out_fname, (stat.S_IRUSR | stat.S_IWUSR |
                                 stat.S_IRGRP | stat.S_IWGRP |
                                 stat.S_IROTH))
        else:
            os.remove(temp_fname)
            sys.stdout.write(u"    no output generated\n")
        # Log file
        log_fname = osp.join(out_dirname,
                             u"{0}.log.json".format(fname_name))
        with open(log_fname, u"w") as log_stream:
            json.dump(log.dump(), log_stream)
    sys.stdout.write(u"\nSynthesis:\n")
    sys.stdout.write(u"  Files to process: {0:d}\n".format(files_number))
    for key in (u"INVALID", u"FAILED", u"ERROR", u"OK"):
        sys.stdout.write(u"  {0}: {1:d} files\n".format(key,
                                                        len(abstract[key])))
        if key != u"OK" and len(abstract[key]) > 0:
            sys.stdout.write(u" ".join(abstract[key]))
            sys.stdout.write(u"\n")
        if key == u"OK" and abstract[u"OK-invalid-input"] > 0:
            sys.stdout.write(
                u"      including {0:d} files with invalid input\n"
                u"".format(abstract[u"OK-invalid-input"]))

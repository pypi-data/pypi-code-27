import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import numpy
import math
import os
import multiprocessing

from .. import utils
from . import mtcnn2

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-d', required=True, help = "Select the directory, where the UCCS image files are stored")
  parser.add_argument('--result-file', '-w', default = "results/UCCS-v2-detection-baseline-%s.txt", help = "Select the file to write the scores into")
  parser.add_argument('--which-set', '-y', default = "validation", choices = ("validation", "test", "sample"), help = "Select the protocol to use")

  parser.add_argument('--parallel', '-P', type=int, help = "If given, images will be processed with the given number of parallel processes")
  parser.add_argument('--gpus', '-g', type=int, nargs='+', help = "If given, the specified GPUs will be used")

  parser.add_argument('--display', '-x', action='store_true', help = "Displays preprocessed images (waits for user keypress); not in parallel mode")
  parser.add_argument('--debug', '-q', type=int, help = "Use only a subset of the data")

  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.parallel is not None and args.display:
    logger.warn("Disabling --display (-x) as we run in parallel mode")
    args.display = False

  try:
    args.result_file = args.result_file % args.which_set
  except:
    pass

  return args


def _parallel(arguments):
  image_files, args, gt_bounding_boxes = arguments

  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else 1
  gpu_id = None if args.gpus is None else args.gpus[(process_id - 1) % len(args.gpus)]

  # load face detector
  if process_id == 1:
    logger.info("Loading MTCNN2 face detector")
  # TODO: take the other parameters from command line
  detector = mtcnn2.MTCNNDetector(gpu_id)

  logger.info("Processing %d images in process %d", len(image_files), process_id)
  detections = {}
  for image_file in image_files:
    try:
      detections[image_file] = []
      image, result = detector.detect_faces(os.path.join(args.data_directory, args.which_set, image_file))
      if result is not None:
        boxes, points, scores = result
        assert len(scores) == len(boxes)
        for i, box in enumerate(boxes):
          detections[image_file].append((box[0], box[1], box[2]-box[0], box[3]-box[1], scores[i][0]))
        logger.debug("Detected %d faces in image %s", len(detections[image_file]), image_file)
      else:
        logger.warn("No face was found for image %s", image_file)

      if args.display:
        # for displaying purposes only
        from matplotlib import pyplot, patches
        pyplot.figure("Detections")
        pyplot.clf()
        pyplot.imshow(image)

        # show detections
        if detections[image_file]:
          min_quality = 0.9
          quality_range = max(1. - min_quality, 1e-4)

          for bbx in detections[image_file]:
            lw = max((bbx[4] - min_quality / quality_range) + 1, 1)
            pyplot.gca().add_patch(patches.Rectangle(bbx[:2], bbx[2], bbx[3], fill=False, color='g', lw=4.*lw))

        # show ground truth
        if gt_bounding_boxes is not None:
          for _,bbx in gt_bounding_boxes[image_file]:
            if bbx is not None:
              pyplot.gca().add_patch(patches.Rectangle(bbx[:2], bbx[2], bbx[3], fill=False, color='r', lw=3, ls=':'))

        input("Detections in image %s; Press Enter to continue" % image_file)
    except Exception as e:
      logger.error("File %s: error %s", image_file, e)

  logger.debug("Finished process %d" % process_id)
  return detections


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)

  # load protocol
  logger.info("Loading UCCS %s protocol", args.which_set)
  data = utils.read_ground_truth(args.data_directory, args.which_set)
  image_names = sorted(data.keys())

  if args.debug:
    # limit the data to the given number of images (debug mode only)
    image_names = image_names[:args.debug]

  if args.parallel is None:
    logger.info("Detecting faces in %d images", len(image_names))
    # no parallelization; process all images sequentially; the ground truth "dataT is used for display purposes only
    detections = _parallel((image_names, args, data))
  else:
    # parallelization; split data into chunks
    logger.info("Detecting faces in %d images using %d parallel processes", len(image_names), args.parallel)
    detections = {}
    pool = multiprocessing.Pool(args.parallel)
    splits = utils.split_data_list_into_parallel(image_names, args.parallel, (args, None))
    # process each chunk in a different process
    for d in pool.imap_unordered(_parallel, splits):
      detections.update(d)
    pool.close()
    pool.join()

  logger.info("Writing result file to %s", args.result_file)
  bob.io.base.create_directories_safe(os.path.dirname(args.result_file))
  with open(args.result_file, "w") as f:
    if command_line_arguments is None:
      import sys
      command_line_arguments = sys.argv
    f.write("# Created using command line: %s\n" % " ".join(command_line_arguments))
    f.write("# FILE,BB_X,BB_Y,BB_WIDTH,BB_HEIGHT,DETECTION_SCORE\n")
    for image in sorted(detections.keys()):
      for bbx in detections[image]:
        f.write("%s,%3.2f,%3.2f,%3.2f,%3.2f,%3.2f\n" % (image, bbx[0], bbx[1], bbx[2], bbx[3], bbx[4]))

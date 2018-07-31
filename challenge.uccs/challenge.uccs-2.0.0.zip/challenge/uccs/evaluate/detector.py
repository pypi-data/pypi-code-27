import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import numpy
import os
import math
import bob.measure
from .. import utils

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-d', required=True, help = "Select the directory, where the UCCS data files are stored")
  parser.add_argument('--result-files', '-r', nargs='+', required=True, help = "Get the file with the UCCS face detection (or recognition) results")
  parser.add_argument('--labels', '-l', nargs='+', help = "Use these labels; if not given, the filenames will be used")
  parser.add_argument('--overlap-threshold', '-t', type=float, default=0.5, help = "The overlap threshold for detected faces to be considered to be detected correctly")
  parser.add_argument('--froc-file', '-w', default = "UCCS-v2-FROC.pdf", help = "The file, where the FROC curve will be plotted into")
  parser.add_argument('--only-present', '-x', action="store_true", help = "Only caluclate the faces for files that have been detected (for debug purposes only)")
  parser.add_argument('--plot-detection-numbers', '-p', action='store_true', help = "If selected, the total number of detected faces will be shown (rather than percentages)")
  parser.add_argument('--log-x', '-s', action='store_true', help = "If selected, plots will be in semilogx")

  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.labels is None:
    args.labels = args.result_files

  if len(args.labels) != len(args.result_files):
    raise ValueError("The number of labels (%d) must be identical to the number of files (%d)" % (len(args.labels), len(args.result_files)))

  return args


def _compare(ground_truth, detection, args):
  faces = len(ground_truth)
  if detection is None:
    return [], [], faces
  # turn into BoundingBox'es
  gt = [utils.bounding_box(g) for _,g in ground_truth]
  dt = [utils.bounding_box(d) for d,_ in detection]

  # compute similarity matrix between detections and ground truth
  similarities = numpy.array([[utils.overlap(g,d) for d in dt] for g in gt])
  # for each detected bounding box, find the gt with the largest overlap
  positives, negatives = [], []

  # for each detection, find the best overlap with the ground truth
  for d in range(len(dt)):
    if numpy.all(similarities[:,d] < args.overlap_threshold):
      # when no overlap is large enough: no face -> negative detection
      negatives.append(detection[d][1])
    else:
      # we have an overlap
      best = numpy.argmax(similarities[:,d])
      if numpy.max(similarities[best,:]) > similarities[best,d] or\
         numpy.count_nonzero(similarities[best,d:] == similarities[best,d]) > 1: # count each negative only once
        # when there is another bounding box with larger overlap with the GT -> negative detection
        # this avoids having lot of overlapping boxes
        negatives.append(detection[d][1])
      else:
        # Best detection with best similarity: this score is a positive
        positives.append(detection[d][1])

  # Find the numbers of ground truth bounding boxes that have not been detected at all
#  missed = sum(numpy.max(similarities[g,:] < args.overlap_threshold) for g in range(len(gt)))

  return positives, negatives, faces


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)

  # read the ground truth bounding boxes of the validation set
  logger.info("Reading UCCS ground-truth from the protocol")
  ground_truth = utils.read_ground_truth(args.data_directory, "validation")

  # read the detections
  results = []
  max_neg = 0
  for r, result_file in enumerate(args.result_files):
    logger.info("Reading detections from %s (%s)", result_file, args.labels[r])
    detections = utils.read_detections(result_file)

    logger.info("Evaluating")
    positives, negatives, faces = [], [], 0.
    for image in ground_truth:
      detection =  detections[image] if image in detections else None
      if detection is None and args.only_present:
        # debug only: remove files that were not processed
        continue
      pos, neg, fac = _compare(ground_truth[image], detection, args)
      positives.extend(pos)
      negatives.extend(neg)
      faces += fac
    logger.info("In total: %d faces, %d detected faces and %d false alarms", faces, len(positives), len(negatives))
    positives = numpy.array(positives)
    negatives = numpy.array(negatives)

    logger.info("Computing FROC curves")
    # compute some thresholds
    if False:
      tmin = min(negatives)
      tmax = max(negatives)
      count = 100
      thresholds = [tmin + float(x)/count * (tmax - tmin) for x in range(count+2)]
    else:
      if args.log_x:
        # get false alarms in a log scale
        base = math.pow(10., 1./8.)
        false_alarm_counts = [math.pow(base,i) for i in range(int(math.log(len(negatives), base)))] + [len(negatives)]
      else:
        false_alarm_counts = list(range(0,len(negatives),1000)) + [len(negatives)]
      fa_values = [float(c) / len(negatives) for c in false_alarm_counts]
      # and compute thresholds
      thresholds = [bob.measure.far_threshold(negatives, [], v, True) for v in fa_values]
      max_neg = numpy.max(negatives)
      thresholds = [t if t <= max_neg else math.nan for t in thresholds]

    false_alarms = []
    detections = []
    for i, threshold in enumerate(thresholds):
      if args.plot_detection_numbers:
        detections.append(sum(bob.measure.correctly_classified_positives(positives, threshold)))
      else:
        detections.append(float(sum(bob.measure.correctly_classified_positives(positives, threshold))) / faces)
      false_alarms.append(len(negatives) - sum(bob.measure.correctly_classified_negatives(negatives, threshold)) if not math.isnan(threshold) else false_alarm_counts[i])

    # to display 0 in a semilogx plot, we have to add a little to the highest threshold
    results.append((detections, false_alarms))
    max_neg = max(max_neg, len(negatives))

  logger.info("Plotting FROC curve(s) to file '%s'", args.froc_file)
  # import matplotlib and set some defaults
  from matplotlib import pyplot
  pyplot.ioff()
  import matplotlib
  matplotlib.rc('text', usetex=True)
  matplotlib.rc('font', family='serif')
  matplotlib.rc('lines', linewidth = 4)
  # increase the default font size
  matplotlib.rc('font', size=18)

  # now, plot
  figure = pyplot.figure(figsize=(7,4.5))
  plotter = pyplot.semilogx if args.log_x else pyplot.plot
  for i, label in enumerate(args.labels):
    plotter(results[i][1], results[i][0], label=label)

  # plot x=y curve
  if args.plot_detection_numbers:
    plotter(results[-1][1], results[-1][1], ":", color=(.6,.6,.6))
  else:
    plotter(results[-1][1], [float(r) / faces for r in results[-1][1]], ":", color=(.6,.6,.6))

  # finalize plot
  if args.log_x:
    pyplot.xticks((1, 10, 100, 1000, 10000, 100000), ('1', '10', '100', '1000', '10000', '100000'))
    pyplot.xlim((1, max_neg))
  else:
    pyplot.xlim((0, max_neg))
  pyplot.grid(True, color=(0.4,0.4,0.4))
#  pyplot.title("FROC curve")
  pyplot.legend(loc=2 if args.log_x else 4, prop={'size':14})

  pyplot.xlabel('False Accepts')
  if args.plot_detection_numbers:
    pyplot.ylim((0, faces))
    pyplot.yticks(range(0, int(faces), 3000))
    pyplot.ylabel('Number of Detections')
  else:
    pyplot.ylim((0, 1))
    pyplot.ylabel('Detection Rate')
  pyplot.tight_layout()
  pyplot.savefig(args.froc_file)

import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import numpy
import math
import os
import multiprocessing
import collections

from .. import utils
from . import mtcnn2, vgg2

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-d', required=True, help = "Select the directory, where image files are stored")
  parser.add_argument('--result-file', '-w', default = "results/UCCS-v2-recognition-baseline-%s.txt", help = "Select the file to write the scores into")
  parser.add_argument('--which-set', '-y', default = 'validation', choices=('validation', 'test'), help = "Which probe images should be used?")

  parser.add_argument('--maximum-scores', '-m', type=int, default=10, help = "Specify, how many scores per probe image should be stored")

  parser.add_argument('--features-file', default='temp/VGG2-Features.hdf5', help = "Set intermediate file, where the features of the gallery are stored")
  parser.add_argument('--models-file', default='temp/VGG2-Models.hdf5', help = "Set intermediate file, where the models are stored")
  parser.add_argument('--probes-file', default='temp/VGG2-Probes-%s.hdf5', help = "Set intermediate file, where the probes are stored")

  parser.add_argument('--parallel', '-P', type=int, help = "If given, images will be processed with the given number of parallel processes")
  parser.add_argument('--gpus', '-g', type=int, nargs='+', help = "If given, the specified GPUs will be used")

  parser.add_argument('--debug', '-q', type=int, help = "Use only the given number of identities")
  parser.add_argument('--force', '-F', action='store_true', help = "If selected, already processed files will be overwritten")


  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.debug is not None:
    temp_dir = "temp-%d" % args.debug
    result_dir = "results-%d" % args.debug
    args.features_file = args.features_file.replace("temp", temp_dir)
    args.models_file = args.models_file.replace("temp", temp_dir)
    args.probes_file = args.probes_file.replace("temp", temp_dir)
    args.result_file = args.result_file.replace("results", result_dir)

  args.probes_file = args.probes_file % args.which_set
  try:
    args.result_file = args.result_file % args.which_set
  except:
    pass

  bob.io.base.create_directories_safe(os.path.dirname(args.features_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.models_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.probes_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.result_file))

  return args



def _bbx(b,q):
  # turns the BoundingBox C++ object into a (picklable) list so that it can be returned through multiprocessing
  return b.left_f, b.top_f, b.size_f[1], b.size_f[0], q


def _extract_features(arguments):
  """Re-detects the faces in the training images -- to be of the same size as we will use later on for the test images"""
  image_names, ground_truth, args = arguments
  is_test = ground_truth is None
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else 1
  gpu_id = None if args.gpus is None else args.gpus[(process_id - 1) % len(args.gpus)]

  # load face detector and feature extractor
  if process_id == 1:
    logger.info("Loading face detector and feature extractor")

  if is_test:
    # TODO: take the other parameters from command line
    detector = mtcnn2.MTCNNDetector(gpu_id)
  else:
    detector = mtcnn2.MTCNNDetector(gpu_id, threshold=(0.1, 0.2, 0.2))
  extractor = vgg2.VGGFace2(gpu_id)

  logger.info("Extracting features from faces in %d training images in process %d", len(image_names), process_id)

  features = collections.defaultdict(list)

  for image_name in image_names:
    image, result = detector.detect_faces(os.path.join(args.data_directory, args.which_set if is_test else "training", image_name))
    if result is not None:
      boxes, points, scores = result
      assert len(scores) == len(boxes)
    else:
      logger.warn("No face was found for image %s", image_name)

    if is_test:
      # test set, store bounding box and feature
      for i, box in enumerate(boxes):
        feature, crop = extractor.get_face_descriptor(image, box)
        features[image_name].append(((box[0], box[1], box[2]-box[0], box[3]-box[1], scores[i][0]), feature))

    else:
      # training set, store features per ground truth subject
      finished_subjects = set()
      for i, box in enumerate(boxes):
        # check, which GT face is the closest
        det = utils.bounding_box((box[0], box[1], box[2]-box[0], box[3]-box[1], scores[i]))
        overlaps = sorted(((utils.overlap(utils.bounding_box(gt), det), subject) for subject, gt in ground_truth[image_name]), key=lambda x:x[0], reverse=True)
        # get the best overlap
        if overlaps[0][0] < 0.5:
          # this does not belong to a subject, use subject value -100
          subject = -100
        else:
          subject = overlaps[0][1]
          if subject in finished_subjects:
            # we only want one feature per subject per image
            continue
        # extract feature
        features[subject].append(extractor.get_face_descriptor(image, box)[0])
        if subject > 0:
          finished_subjects.add(subject)

  return features



def extract_features(dataset, pool, args, is_training):
  """Extracts deep features for each bounding box in each image"""
  # select, which function to use for feature extraction
  image_names = sorted(dataset.keys())
  ground_truth = dataset if is_training else None
  logger.info("Extracting %s features from %d images", "training" if is_training else "test", len(dataset))
  # extract LBPHS features for all images
  if pool is None:
    features = _extract_features((image_names, ground_truth, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    splits = utils.split_data_list_into_parallel(image_names, args.parallel, (ground_truth, args))
    features = {}
    for extracted in pool.imap_unordered(_extract_features, splits):
      for k,v in extracted.items():
        if k not in features:
          features[k] = []
        features[k].extend(v)

  return features


def enroll(features):
  """Enrolls models by averaging the features for each subject"""
  # average features
  models = {subject: numpy.mean(feature, axis=0) for subject, feature in features.items()}
  # normalize models
  return {subject: model / numpy.linalg.norm(model) for subject, model in models.items()}


def _compare(model, probe):
  return numpy.dot(model, probe)

def _scores(arguments):
  probes, models, args  = arguments
  scores_for_probes = {}
  for image, probe_features in probes.items():
    scores_for_probes[image] = []
    scores = {}
    for probe in probe_features:
      for subject, model in models.items():
        scores[subject] = _compare(model, probe)
      # handle -100 scores
      if -100 in scores:
        if -1 in scores:
          if scores[-100] > scores[-1]:
            scores[-1] = scores[-100]
        else:
          scores[-1] = scores[-100]
        del scores[-100]

      # keep only maximum scores
      lowest_score = sorted(scores.values())[-args.maximum_scores]
      if -1 in scores:
        # when we predict -1 in our scores, the -1 score should be the lowest to be written
        lowest_score = max(lowest_score, scores[-1])
      scores_for_probes[image].append({subject : score for subject,score in scores.items() if score >= lowest_score})
  return scores_for_probes


def compute_scores(models, probes, pool, args):
  logger.info("Computing scores between %s models and %d probes", len(models), len(probes))
  # extract training features
  if pool is None:
    scores = _scores((probes, models, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    probe_splits = utils.split_data_dict_into_parallel(probes, args.parallel, (models, args))
    scores = {}
    for score in pool.imap_unordered(_scores, probe_splits):
      scores.update(score)

  return scores

def limit(data, subjects, use_unknowns=False):
  tmp = {}
  unknown_counter = 0
  max_unknowns = len(subjects) * 10
  for f,v in data.items():
    if use_unknowns and v[0][0] == -1 and unknown_counter < max_unknowns:
      tmp[f] = v
      unknown_counter += 1
    elif v[0][0] in subjects:
      tmp[f] = v
  return tmp


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)

  # for the training set, we use all available data
  training = utils.read_ground_truth(args.data_directory, "training")
  # for the probes, we will use only the image names
  probe = utils.read_ground_truth(args.data_directory, args.which_set)

  if args.debug is not None:
    subjects = set(range(1,args.debug+1))
    training = limit(training, subjects)
    probe = limit(probe, subjects, True)
    logger.info("Limited to %d training and %d probe images of %d subjects", len(training), len(probe), len(subjects))

  pool = None if args.parallel is None else multiprocessing.Pool(args.parallel)

  if not os.path.exists(args.features_file) or args.force:
    logger.info("Detecting faces and extracting features of the training set")
    # re-detect training faces and extract features; this might take some time
    training_features = extract_features(training, pool, args, is_training=True)
    logger.info("Writing features to file %s", args.features_file)
    h = bob.io.base.HDF5File(args.features_file, 'w')
    for subject, features in training_features.items():
      h.set(str(subject), features)
  else:
    logger.info("Reading features from file %s", args.features_file)
    h = bob.io.base.HDF5File(args.features_file)
    training_features = {int(f): h.get(f) for f in h.keys(relative=True)}

  if not os.path.exists(args.models_file) or args.force:
    # enroll models from training set features
    logger.info("Enrolling models")
    models = enroll(training_features)
    logger.info("Writing models to file %s", args.models_file)
    h = bob.io.base.HDF5File(args.models_file, 'w')
    for subject, model in models.items():
      h.set(str(subject), model)
  else:
    logger.info("Reading models from file %s", args.models_file)
    h = bob.io.base.HDF5File(args.models_file, 'r')
    models = {int(f): h.get(f) for f in h.keys(relative=True)}

  if not os.path.exists(args.probes_file) or args.force:
    # detect faces and extract probe features; this might take a while
    probe_features = extract_features(probe, pool, args, is_training=False)

    # align features to be projected
    bounding_boxes = {image : [feature[0] for feature in val] for image, val in probe_features.items()}
    probes = {image : [feature[1] for feature in val] for image, val in probe_features.items()}

    # and project them
    logger.info("Writing probes from %d images to file %s", len(probes), args.probes_file)
    h = bob.io.base.HDF5File(args.probes_file, 'w')
    for filename, probe in probes.items():
      h.set(filename.replace("/","$"), probe)
      h.set(filename.replace("/","$")+"-bbxs", bounding_boxes[filename])

  else:
    logger.info("Reading probes from file %s", args.probes_file)
    h = bob.io.base.HDF5File(args.probes_file, 'r')
    probes = {f.replace("$","/"): h.get(f) for f in h.keys(relative=True) if '-bbxs' not in f}
    bounding_boxes = {f.replace("$","/").replace("-bbxs",""): h.get(f) for f in h.keys(relative=True) if '-bbxs' in f}


  # compute similarities between model and probes
  scores = compute_scores(models, probes, pool, args)

  logger.info("Writing scores to score file %s", args.result_file)
  bob.io.base.create_directories_safe(os.path.dirname(args.result_file))
  with open(args.result_file, 'w') as f:
    if command_line_arguments is None:
      import sys
      command_line_arguments = sys.argv
    f.write("# Created using command line: %s\n" % " ".join(command_line_arguments))
    f.write("# FILE,BB_X,BB_Y,BB_WIDTH,BB_HEIGHT,DETECTION_SCORE,SUBJECT_ID_1,RECOGNITION_SCORE_1,SUBJECT_ID_2,RECOGNITION_SCORE_2,SUBJECT_ID_3,RECOGNITION_SCORE_3,...\n")
    for probe_image in sorted(scores.keys()):
      for p, values in enumerate(scores[probe_image]):
        bbx = bounding_boxes[probe_image][p]
        f.write("%s,%3.2f,%3.2f,%3.2f,%3.2f,%3.2f" % (probe_image, bbx[0], bbx[1], bbx[2], bbx[3], bbx[4]))
        for subject, value in values.items():
          f.write(",%d,%1.6f" % (subject, value))
        f.write("\n")

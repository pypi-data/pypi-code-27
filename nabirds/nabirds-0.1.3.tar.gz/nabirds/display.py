#!/usr/bin/env python
if __name__ != '__main__': raise Exception("Do not import me!")

from argparse import ArgumentParser
import logging
import numpy as np

from nabirds import Dataset, NAB_Annotations, CUB_Annotations
from nabirds.dataset import visible_part_locs, visible_crops, reveal_parts
import matplotlib.pyplot as plt

def init_logger(args):
	fmt = "%(levelname)s - [%(asctime)s] %(filename)s:%(lineno)d [%(funcName)s]: %(message)s"
	logging.basicConfig(
		format=fmt,
		level=getattr(logging, args.loglevel.upper(), logging.DEBUG),
		filename=args.logfile or None,
		filemode="w")

def main(args):
	init_logger(args)

	annotation_cls = dict(
		nab=NAB_Annotations,
		cub=CUB_Annotations)

	logging.info("Loading \"{}\" annnotations from \"{}\"".format(args.dataset, args.data))
	annot = annotation_cls.get(args.dataset.lower())(args.data)

	uuids = getattr(annot, "{}_uuids".format(args.subset.lower()))
	data = Dataset(uuids, annot)
	n_images = len(data)
	logging.info("Found {} images in the {} subset".format(n_images, args.subset))

	for i in range(n_images):
		if i + 1 <= args.start: continue

		im, parts, label = data[i]

		idxs, xy = visible_part_locs(parts)

		logging.debug(label)
		logging.debug(idxs)

		fig1 = plt.figure(figsize=(16,9))
		ax = fig1.add_subplot(2,1,1)

		ax.imshow(im)
		ax.scatter(*xy, marker="x", c=idxs)

		ax = fig1.add_subplot(2,1,2)
		ax.imshow(reveal_parts(im, xy, ratio=args.ratio))
		ax.scatter(*xy, marker="x", c=idxs)

		fig2 = plt.figure(figsize=(16,9))
		n_parts = parts.shape[0]
		rows, cols = (2,6) if args.dataset.lower() == "nab" else (3,5)
		for j, crop in enumerate(visible_crops(im, parts, ratio=args.ratio), 1):
			ax = fig2.add_subplot(rows, cols, j)
			ax.imshow(crop)

			middle = crop.shape[0] / 2
			ax.scatter(middle, middle, marker="x")

		plt.show()
		plt.close(fig1)
		plt.close(fig2)

		if i+1 >= args.start + args.n_images: break

parser = ArgumentParser()

parser.add_argument("data",
	help="Folder containing the dataset with images and annotation files",
	type=str)

parser.add_argument("--dataset",
	help="Possible datasets: NAB, CUB",
	choices=["cub", "nab"],
	default="nab", type=str)

parser.add_argument("--subset",
	help="Possible subsets: train, test",
	choices=["train", "test"],
	default="train", type=str)

parser.add_argument("--start", "-s",
	help="Image id to start with",
	type=int, default=0)

parser.add_argument("--n_images", "-n",
	help="Number of images to display",
	type=int, default=10)

parser.add_argument("--ratio",
	help="Part extraction ratio",
	type=float, default=.2)

parser.add_argument(
	'--logfile', type=str, default='',
	help='File for logging output')

parser.add_argument(
	'--loglevel', type=str, default='INFO',
	help='logging level. see logging module for more information')

main(parser.parse_args())

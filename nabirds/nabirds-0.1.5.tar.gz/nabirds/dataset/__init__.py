from imageio import imread
import numpy as np


class Dataset(object):
	def __init__(self, uuids, annotations):
		super(Dataset, self).__init__()
		self.uuids = uuids
		self._annot = annotations

	def __len__(self):
		return len(self.uuids)

	def _get(self, method, i):
		return getattr(self._annot, method)(self.uuids[i])



	def get_example(self, i, mode="RGB"):
		methods = ["image", "parts", "label"]
		im_path, parts, label = [self._get(m, i) for m in methods]
		return imread(im_path, pilmode=mode), parts, label

	__getitem__  = get_example

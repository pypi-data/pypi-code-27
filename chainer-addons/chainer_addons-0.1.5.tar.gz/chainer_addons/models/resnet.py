import numpy as np
import chainer.links as L
import chainer.functions as F

from chainer.links.model.vision.resnet import prepare
from functools import partial

from chainer_addons.models import PretrainedModelMixin


class ResnetLayers(PretrainedModelMixin, L.ResNet50Layers):

	class meta:
		classifier_layers = ["fc6"]
		conv_map_layer = "res5"
		feature_layer = "pool5"
		feature_size = 2048
		n_conv_maps = 2048
		input_size = 448
		mean = np.array([103.063,  115.903,  123.152], dtype=np.float32).reshape(3,1,1)

		prepare_func = prepare

	@staticmethod
	def pooling(x):
		n, channel, rows, cols = x.data.shape
		h = F.average_pooling_2d(x, (rows, cols), stride=1)
		h = F.reshape(h, (n, channel))
		return h

	def __init__(self, pretrained_model, n_classes):
		if pretrained_model == "auto":
			super(ResnetLayers, self).__init__(pretrained_model=pretrained_model)
		else:
			super(ResnetLayers, self).__init__(pretrained_model=None)

		with self.init_scope():
			self.load_pretrained(pretrained_model, n_classes)

	@property
	def _links(self):
		links = [
				('conv1', [self.conv1, self.bn1, F.relu]),
				('pool1', [partial(F.max_pooling_2d, ksize=3, stride=2)]),
				('res2', [self.res2]),
				('res3', [self.res3]),
				('res4', [self.res4]),
				('res5', [self.res5]),
				('pool5', [ResnetLayers.pooling])]
		if hasattr(self, "fc6"):
			links +=[
				('fc6', [self.fc6]),
				('prob', [F.softmax]),
			]

		return links

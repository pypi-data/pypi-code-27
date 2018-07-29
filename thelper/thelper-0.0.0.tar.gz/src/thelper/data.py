import logging
import os
from abc import abstractmethod
from collections import Counter
from copy import copy

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.utils.data
import torchvision.transforms
import torchvision.utils

import thelper.transforms
import thelper.utils

data_logger = logging.getLogger("thelper.data")


class DataConfig(object):
    def __init__(self,config):
        self.logger = logging.getLogger("thelper.data.DataConfig")
        self.logger.debug("loading data config")
        if not isinstance(config,dict):
            raise AssertionError("input config should be dict")
        if "batch_size" not in config or not config["batch_size"]:
            raise AssertionError("data config missing 'batch_size' field")
        self.batch_size = config["batch_size"]
        self.shuffle = thelper.utils.str2bool(config["shuffle"]) if "shuffle" in config else False
        self.seed = config["seed"] if "seed" in config and isinstance(config["seed"],(int,str)) else None
        self.workers = config["workers"] if "workers" in config and config["workers"]>=0 else 1
        self.pin_memory = thelper.utils.str2bool(config["pin_memory"]) if "pin_memory" in config else False
        self.drop_last = thelper.utils.str2bool(config["drop_last"]) if "drop_last" in config else False
        self.train_augments = None
        if "train_augments" in config and config["train_augments"]:
            self.train_augments = thelper.transforms.load_transforms(config["train_augments"])
        if "train_split" not in config or not config["train_split"]:
            raise AssertionError("data config missing 'train_split' field")
        self.train_split = config["train_split"]
        if any(ratio<0 or ratio>1 for ratio in self.train_split.values()):
            raise AssertionError("split ratios must be in [0,1]")
        if "valid_split" not in config or not config["valid_split"]:
            raise AssertionError("data config missing 'valid_split' field")
        self.valid_split = config["valid_split"]
        if any(ratio<0 or ratio>1 for ratio in self.valid_split.values()):
            raise AssertionError("split ratios must be in [0,1]")
        if "test_split" not in config or not config["test_split"]:
            raise AssertionError("data config missing 'test_split' field")
        self.test_split = config["test_split"]
        if any(ratio<0 or ratio>1 for ratio in self.test_split.values()):
            raise AssertionError("split ratios must be in [0,1]")
        self.total_usage = Counter(self.train_split)+Counter(self.valid_split)+Counter(self.test_split)
        for name,usage in self.total_usage.items():
            if usage>0 and usage!=1:
                self.logger.warning("dataset split for '%s' does not sum 1; will normalize..."%name)
                self.train_split[name] /= usage
                self.valid_split[name] /= usage
                self.test_split[name] /= usage

    def get_idx_split(self,dataset_map_size):
        self.logger.debug("loading dataset split & normalizing ratios")
        for name in self.total_usage:
            if name not in dataset_map_size:
                raise AssertionError("dataset '%s' does not exist"%name)
        indices = {name:list(range(size)) for name,size in dataset_map_size.items()}
        if self.shuffle:
            np.random.seed(self.seed)
            for idxs in indices.values():
                np.random.shuffle(idxs)
        train_idxs,valid_idxs,test_idxs = {},{},{}
        offsets = dict.fromkeys(self.total_usage,0)
        for name in self.total_usage.keys():
            for idxs_map,ratio_map in zip([train_idxs,valid_idxs,test_idxs],[self.train_split,self.valid_split,self.test_split]):
                if name in ratio_map:
                    count = int(round(ratio_map[name]*dataset_map_size[name]))
                    if count<0:
                        raise AssertionError("ratios should be non-negative values!")
                    elif count<1:
                        self.logger.warning("split ratio for '%s' too small, sample set will be empty"%name)
                    begidx = offsets[name]
                    endidx = min(begidx+count,dataset_map_size[name])
                    idxs_map[name] = indices[name][begidx:endidx]
                    offsets[name] = endidx
        return train_idxs,valid_idxs,test_idxs

    def get_data_split(self,dataset_templates):
        dataset_size_map = {name:len(dataset) for name,dataset in dataset_templates.items()}
        train_idxs,valid_idxs,test_idxs = self.get_idx_split(dataset_size_map)
        train_data,valid_data,test_data,loaders = [],[],[],[]
        for loader_idx,(idxs_map,datasets) in enumerate(zip([train_idxs,valid_idxs,test_idxs],
                                                            [train_data,valid_data,test_data])):
            for name,sample_idxs in idxs_map.items():
                dataset = copy(dataset_templates[name])
                if loader_idx==0 and self.train_augments:
                    if dataset.transforms:
                        dataset.transforms = torchvision.transforms.Compose([dataset.transforms,copy(self.train_augments)])
                    else:
                        dataset.transforms = copy(self.train_augments)
                dataset.sampler = SubsetRandomSampler(sample_idxs)
                datasets.append(dataset)
            if len(datasets)>1:
                dataset = torch.utils.data.ConcatDataset(datasets)
                sampler = torch.utils.data.sampler.RandomSampler(dataset)
                loaders.append(torch.utils.data.DataLoader(dataset,
                                                           batch_size=self.batch_size,
                                                           sampler=sampler,
                                                           num_workers=self.workers,
                                                           pin_memory=self.pin_memory,
                                                           drop_last=self.drop_last))
            else:
                loaders.append(torch.utils.data.DataLoader(datasets[0],
                                                           batch_size=self.batch_size,
                                                           num_workers=self.workers,
                                                           pin_memory=self.pin_memory,
                                                           drop_last=self.drop_last))
        train_loader,valid_loader,test_loader = loaders
        return train_loader,valid_loader,test_loader


def load_dataset_templates(config,root):
    templates = {}
    # todo : check compatibility between predicted types?
    for dataset_name,dataset_config in config.items():
        if "type" not in dataset_config:
            raise AssertionError("missing field 'type' for instantiation of dataset '%s'"%dataset_name)
        type = thelper.utils.import_class(dataset_config["type"])
        if "params" not in dataset_config:
            raise AssertionError("missing field 'params' for instantiation of dataset '%s'"%dataset_name)
        params = thelper.utils.keyvals2dict(dataset_config["params"])
        transforms = None
        if "transforms" in dataset_config and dataset_config["transforms"]:
            transforms = thelper.transforms.load_transforms(dataset_config["transforms"])
        templates[dataset_name] = type(params,name=dataset_name,root=root,transforms=transforms)
    return templates


def visualize_classif(sample,pred=None):
    if not isinstance(sample,dict):
        raise AssertionError("expected dict-based sample")
    if "image" not in sample or "label" not in sample:
        raise AssertionError("missing classification-related fields in sample dict")
    labels = sample["label"]
    if not isinstance(labels,list):
        raise AssertionError("expected classification labels to be in list format")
    # here we assume the sample's data has been tensor'd (so images are 4D, BxCxHxW)
    images = sample["image"].numpy().copy()
    if images.ndim!=4:
        raise AssertionError("unexpected dimension count for input images tensor")
    if images.shape[0]!=len(labels):
        raise AssertionError("images/labels count mismatch")
    images = np.transpose(images,(0,2,3,1))  # BxCxHxW to BxHxWxC
    masks = sample["mask"].numpy().copy() if "mask" in sample else None
    if masks is not None:
        # masks should have same dim count, but 2nd always equal to 1 (single channel)
        if masks.ndim!=4 or masks.shape[1]!=1:
            raise AssertionError("image/mask ndim mismatch")
        if (images.shape[0:3]!=np.asarray(masks.shape)[[0,2,3]]).any():
            raise AssertionError("image/mask shape mismatch")
    image_list = []
    for batch_idx in range(images.shape[0]):
        image = images[batch_idx,...]
        if image.ndim!=3:
            raise AssertionError("indexing should return a pre-squeezed array")
        if image.shape[2]==2:
            image = np.dstack((image,image[:,:,0]))
        elif image.shape[2]>3:
            image = image[...,:3]
        image_normalized = np.empty_like(image,dtype=np.uint8).copy()  # copy needed here due to ocv 3.3 bug
        cv.normalize(image,image_normalized,0,255,cv.NORM_MINMAX,dtype=cv.CV_8U)
        image_list.append(image_normalized)
    thelper.utils.draw_classifs(image_list,labels,labels_pred=pred)  # normalize & pass mask to draw func also? todo
    plt.waitforbuttonpress()


class SubsetRandomSampler(torch.utils.data.sampler.SubsetRandomSampler):
    def __init__(self,indices):
        # the difference between this class and pytorch's default one is the __getitem__ member that provides raw indices
        super().__init__(indices)

    def __getitem__(self,idx):
        # we do not reshuffle here, as we cannot know when the cycle is 'reset'; indices should thus come in pre-shuffled
        return self.indices[idx]


class Dataset(torch.utils.data.Dataset):
    def __init__(self,name=None,root=None,transforms=None):
        if not root:
            root = "./"
        if not os.path.exists(root) or not os.path.isdir(root):
            raise AssertionError("dataset root folder at '%s' does not exist"%root)
        self.name = name
        self.root = root
        self.transforms = transforms
        self._sampler = None
        self.samples = None  # must be filled by the derived class

    # todo: add method to reset sampler shuffling when epoch complete?

    @property
    def sampler(self):
        return self._sampler

    @sampler.setter
    def sampler(self,newsampler):
        if newsampler:
            sample_iter = iter(newsampler)
            try:
                while True:
                    sample_idx = next(sample_iter)
                    if sample_idx<0 or sample_idx>len(self.samples):
                        raise AssertionError("sampler provides oob indices for assigned dataset")
            except StopIteration:
                pass
        self._sampler = newsampler

    def total_size(self):
        # bypasses sampler, if one is active
        return len(self.samples)

    def __len__(self):
        # if a sampler is active, return its subset size
        if self.sampler:
            return len(self.sampler)
        return len(self.samples)

    def __iter__(self):
        if not self.sampler:
            for idx in range(len(self.samples)):
                yield self[idx]
        else:
            for idx in self.sampler:
                yield self[idx]

    @abstractmethod
    def __getitem__(self,idx):
        raise NotImplementedError

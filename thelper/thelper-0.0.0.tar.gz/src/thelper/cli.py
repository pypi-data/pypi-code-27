"""
Command-line module, for use with __main__ entrypoint or external apps.
"""

import argparse
import json
import logging
import os
from copy import copy

import torch

import thelper

logging.basicConfig(level=logging.INFO)


def train(config,resume,data_root,log_path=None,log_level=logging.INFO,display_graphs=False):
    print(__name__)
    logger = logging.getLogger("thelper.cli")
    logger.propagate = 0
    format = "[%(asctime)s - %(name)s - %(process)s:%(thread)s] %(levelname)s : %(message)s"
    logger_format = logging.Formatter(format)
    if log_path:
        logger_fh = logging.FileHandler(log_path)
        logger_fh.setLevel(logging.DEBUG)
        logger_fh.setFormatter(logger_format)
        logger.addHandler(logger_fh)
    logger_ch = logging.StreamHandler()
    logger_ch.setLevel(log_level)
    logger_ch.setFormatter(logger_format)
    logger.addHandler(logger_ch)
    logger.info("main entrypoint")

    # load dataset templates & parse folder structure
    logger.debug("loading datasets")
    if "datasets" not in config or not config["datasets"]:
        raise AssertionError("config missing 'datasets' field (can be dict or str)")
    datasets_config = config["datasets"]
    if isinstance(datasets_config,str):
        if os.path.isfile(datasets_config) and os.path.splitext(datasets_config)[1]==".json":
            datasets_config = json.load(open(datasets_config))
        else:
            raise AssertionError("'datasets' string should point to valid json file")
    if not isinstance(datasets_config,dict):
        raise AssertionError("invalid datasets config type")
    dataset_templates = thelper.data.load_dataset_templates(datasets_config,data_root)

    # load data config & split datasets
    if "data_config" not in config or not config["data_config"]:
        raise AssertionError("config missing 'data_config' field")
    data_config = thelper.data.DataConfig(config["data_config"])
    train_loader,valid_loader,test_loader = data_config.get_data_split(dataset_templates)

    if display_graphs and logger.isEnabledFor(logging.DEBUG):
        train_loader_copy = copy(train_loader)
        data_iter = iter(train_loader_copy)
        # noinspection PyUnresolvedReferences
        data_sample = data_iter.next()
        thelper.data.visualize_classif(data_sample)

    # prep output folders @@@@ TODO MOVE TO TRAINER, HAS PARAM IN CFG ALREADY
    checkpoint_path = os.path.join(data_root,"saved")
    if os.path.isfile(checkpoint_path):
        raise AssertionError("cannot create checkpoint output directory at '%s'"%checkpoint_path)
    elif not os.path.exists(checkpoint_path):
        os.mkdir(checkpoint_path)

    # model = eval(config['arch'])(config['model'])
    # model.summary()
    # loss = eval(config['loss'])
    # metrics = [eval(metric) for metric in config['metrics']]
    # path = os.path.join(config['trainer']['save_dir'],config['name'])
    # assert not os.path.exists(path),"Path {} already exists!".format(path)
    # trainer = Trainer(model,loss,metrics,
    #                   resume=resume,
    #                   config=config,
    #                   data_loader=data_loader,
    #                   valid_data_loader=valid_data_loader,
    #                   train_logger=train_logger)
    # trainer.train()
    raise NotImplementedError


def main(args=None):
    ap = argparse.ArgumentParser(description='thelper model trainer application')
    input_group = ap.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-c","--config",type=str,help="path to the training configuration file")
    input_group.add_argument("-r","--resume",type=str,help="path to the checkpoint to resume training from")
    input_group.add_argument("--version",default=False,action="store_true",help="prints the version of the library and exits")
    ap.add_argument("-l","--log",default="train.log",type=str,help="path to the output log file (default: './train.log')")
    ap.add_argument("-v","--verbose",action="count",default=0,help="set logging terminal verbosity level (additive)")
    ap.add_argument("-g","--display-graphs",action="store_true",default=False,help="toggles whether graphs should be displayed or not")
    ap.add_argument("-d","--data-root",default="./data/",type=str,help="path to the data root directory for parsing datasets")
    args = ap.parse_args(args=args)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)
    if args.verbose>2:
        log_level = logging.NOTSET
    elif args.verbose>1:
        log_level = logging.DEBUG
    elif args.verbose==1:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    root_logger.info("cli entrypoint")
    if args.version:
        print(thelper.__version__)
        return
    root_logger.debug("checking dataset root '%s'..."%args.data_root)
    if not os.path.exists(args.data_root) or not os.path.isdir(args.data_root):
        raise AssertionError("invalid data root folder at '%s'; please specify the correct path via --data-root=PATH")
    config = None
    if args.resume is not None:
        config = torch.load(args.resume)['config']
        if not config:
            raise AssertionError("torch checkpoint loading failed")
    elif args.config is not None:
        config = json.load(open(args.config))
        if "name" not in config or not config["name"]:
            raise AssertionError("model configuration must be named")
    root_logger.info("parsed config '%s' from cli entrypoint"%config["name"])
    train(config,args.resume,args.data_root,log_path=args.log,log_level=log_level,display_graphs=args.display_graphs)

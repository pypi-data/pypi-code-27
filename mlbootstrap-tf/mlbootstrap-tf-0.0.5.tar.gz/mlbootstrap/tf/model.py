from mlbootstrap.model import BasicModel
import tensorflow as tf
import os
import yaml
from tqdm import tqdm
import json
import datetime

_MODEL_STATUS_FILENAME = 'model_status.yaml'


class BasicTfModel(BasicModel):
    def __init__(self):
        super().__init__()

        self.sess: tf.Session = None
        self.saver: tf.train.Saver = None
        self.global_step = 0

    def train(self):
        self._restore_model_settings()
        self._build_graph('train')
        self._create_session()
        self._restore_checkpoint()

        print(json.dumps(self._config, indent=2))
        print()
        print('Start training ...')

        training_params = self.training_parameters()

        epoch = training_params.epoch

        for e in range(1, epoch + 1):
            print()
            learning_rate = training_params.learning_rate
            print(
                '----- Epoch {}/{} ; (learning_rate={}) -----'.format(e, epoch, learning_rate))

            tic = datetime.datetime.now()
            batches = self._get_batches('train')
            for batch in batches:
                self.global_step += 1
                self._train_step(batch)

                if self.global_step % training_params.save_interval == 0:
                    if self._validate():
                        self._save_checkpoint()

            toc = datetime.datetime.now()
            print('Epoch finished in {}'.format(toc - tic))

    def _build_graph(self, mode: str):
        raise NotImplementedError

    def _validate(self):
        raise NotImplementedError

    def _get_batches(self, mode: str):
        raise NotImplementedError

    def _train_step(self, batch):
        raise NotImplementedError

    def _restore_model_settings(self):
        path = self.model_dir()
        os.makedirs(path, exist_ok=True)
        status_path = os.path.join(path, _MODEL_STATUS_FILENAME)

        if os.path.exists(status_path):
            with open(status_path, 'r') as stream:
                model_status = yaml.load(stream)
                self.global_step = model_status['global_step']
                self._config['hyperparameter'] = model_status['hyperparameter']

    def _create_session(self):
        self.sess = tf.Session(config=tf.ConfigProto(
            allow_soft_placement=True,
            gpu_options=tf.GPUOptions(allow_growth=True)
        ))
        self.saver = tf.train.Saver()

    def _restore_checkpoint(self):
        path = self.model_dir()
        os.makedirs(path, exist_ok=True)
        status_path = os.path.join(path, _MODEL_STATUS_FILENAME)

        if os.path.exists(status_path):
            ckpt = tf.train.get_checkpoint_state(path)
            if ckpt and ckpt.model_checkpoint_path:
                self.saver.restore(self.sess, ckpt.model_checkpoint_path)
            else:
                print('No checkpoint found')
                exit(1)
        else:
            self.sess.run(tf.global_variables_initializer())

    def _save_checkpoint(self):
        tqdm.write("Checkpoint reached: saving model (don't stop the run) ...")

        path = self.model_dir()
        os.makedirs(path, exist_ok=True)
        self._save_model_status(path)

        model_path = os.path.join(path, 'model')
        self.saver.save(self.sess, model_path, global_step=self.global_step)
        tqdm.write('Model saved.')

    def _save_model_status(self, path: str):
        model_status = {
            'hyperparameter': self.hyperparameters().__dict__,
            'global_step': self.global_step
        }
        status_path = os.path.join(path, _MODEL_STATUS_FILENAME)
        with open(status_path, 'w') as stream:
            yaml.dump(model_status, stream)

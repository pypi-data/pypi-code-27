from os import path
import pickle

import keras.callbacks as callbacks


class EpochHistory(callbacks.History):
    def __init__(self, epoch=None, file=None):
        super(EpochHistory, self).__init__()
        self.epoch = epoch or []
        self.file = file

    def on_train_begin(self, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        self.epoch.append(epoch)
        self.save()

    def on_train_end(self, logs=None):

        self.save()

    def get_initial_epoch(self):
        if self.epoch:
            return self.epoch[-1] + 1
        else:
            return 0

    def save(self, file=None):
        file = file or self.file
        if file is None:
            return
        with open(file, 'wb') as f:
            pickle.dump(self.epoch, f)

    @classmethod
    def load(cls, file):
        if not path.exists(file):
            return cls(file=file)

        with open(file, 'rb') as f:
            epoch = pickle.load(f)
        epoch_hist = cls(epoch=epoch, file=file)

        return epoch_hist

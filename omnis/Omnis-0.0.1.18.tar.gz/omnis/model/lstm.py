from keras import models
from keras.layers import Input, Dense
from keras import layers

from .model import Model

from ..lib.text_lib import *


class LSTM(Model):
    def __init__(self, input_shape = None, model_path = None, class_dictionary_path = None):
        """Initializes a LSTM model.
        
        Arguments:
            Model {class} -- A super class of neural network models.
        
        Keyword Arguments:
            input_shape {tuple} -- An input shape of the neural network. You must specify this you want to initialize a new model. (default: {None})
            model_path {str} -- A path of model file. (default: {None})
            class_dictionary_path {str or None} -- A path of class_dictionary file. (default: {None})
        
        Raises:
            ValueError -- Raises ValueError if both input_shape and model_path is not specified.
        """
        if type(model_path) != type(None):
            Model.__init__(self, model_path, class_dictionary_path)
        if type(input_shape) != type(None):
            Model.__init__(self)
            self.input_shape = input_shape
        else:
            raise ValueError('you must specifiy input_shape if you want to initialize a new model')

    def create_model(self, lstm_units, num_classes):
        """Creates a deep lstm model.
        
        Arguments:
            lstm_units {int} -- Positive integer, dimensionality of the output space.
            num_classes {int} -- [description]
        """
        input_layer = Input(shape=self.input_shape)
        lstm1 = layers.LSTM(lstm_units)(input_layer)
        output_layer = Dense(num_classes, activation='softmax')(lstm1)    
        self.model = models.Model(inputs=input_layer, outputs=output_layer)

    def train(self,
            x,
            y,
            batch_size = None,
            steps_per_epoch = None,
            epochs = 1,
            verbose = 1,
            callbacks = None,
            shuffle = True):
            self.model.fit(x, y, batch_size=batch_size, steps_per_epoch=steps_per_epoch, epochs = epochs, verbose = verbose, callbacks = callbacks, shuffle = shuffle)


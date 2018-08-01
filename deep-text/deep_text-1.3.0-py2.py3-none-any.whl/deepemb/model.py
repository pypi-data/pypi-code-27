from abc import abstractmethod
import numpy as np
import tensorflow as tf
from common import utils
from common.model import BaseModel
from deepemb.default_custom import DefaultSkipThoughtTransform


class DeepEmbModel(BaseModel):
    def __init__(self, session, transformer, config):
        super(DeepEmbModel, self).__init__(session, transformer, config)
        self.doc_vector = None

    @abstractmethod
    def vectors(self, docs):
        pass


class GraphSkipThoughtModel(DeepEmbModel):
    def __init__(self, model_path, config, TransformClass=None):
        if TransformClass is None:
            super(GraphSkipThoughtModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), DefaultSkipThoughtTransform(config), config)
        else:
            super(GraphSkipThoughtModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), TransformClass(config), config)
        self.transformer.load_pre_data()
        self.session.as_default()

        self.input = self.session.graph.get_tensor_by_name('encode:0')
        self.input_lengths = self.session.graph.get_tensor_by_name('input_lengths:0')

        self.output_prev_input = self.session.graph.get_tensor_by_name('output_prev_input:0')
        self.output_prev_target = self.session.graph.get_tensor_by_name('output_prev_target:0')
        self.output_prev_lengths = self.session.graph.get_tensor_by_name('output_prev_lengths:0')

        self.output_post_input = self.session.graph.get_tensor_by_name('output_post_input:0')
        self.output_post_target = self.session.graph.get_tensor_by_name('output_post_target:0')
        self.output_post_lengths = self.session.graph.get_tensor_by_name('output_post_lengths:0')

        self.input_keep_prob = self.session.graph.get_tensor_by_name("input_keep_prob:0")
        self.output_keep_prob = self.session.graph.get_tensor_by_name("output_keep_prob:0")

        self.doc_vector = self.session.graph.get_tensor_by_name("encoder/rnn/while/Exit_2:0")

    def vectors(self, docs):
        doc_ids = self.transformer.transform_parts(docs)
        doc_lens = np.array([len(d) for d in doc_ids])
        feed_dict = {self.input: doc_ids,
                     self.input_lengths: doc_lens,
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0}

        return self.session.run([self.doc_vector], feed_dict=feed_dict)[0]


import tensorflow as tf
import logging

from common.embedding_types import EmbeddingType
from .model import DeepEmbModel


class SkipThought(DeepEmbModel):
    def __init__(self, session, transformer, config):
        super(SkipThought, self).__init__(session, transformer, config)
        self.input = tf.placeholder(tf.int32, shape=[None, None], name='encode')
        self.input_lengths = tf.placeholder(tf.int32, shape=[None, ], name='input_lengths')

        self.output_prev_input = tf.placeholder(tf.int32, shape=[None, None], name='output_prev_input')
        self.output_prev_target = tf.placeholder(tf.int32, shape=[None, None], name='output_prev_target')
        self.output_prev_lengths = tf.placeholder(tf.int32, shape=[None, ], name='output_prev_lengths')

        self.output_post_input = tf.placeholder(tf.int32, shape=[None, None], name='output_post_input')
        self.output_post_target = tf.placeholder(tf.int32, shape=[None, None], name='output_post_target')
        self.output_post_lengths = tf.placeholder(tf.int32, shape=[None, ], name='output_post_lengths')

        self.input_keep_prob = tf.placeholder(tf.float32, name="input_keep_prob")
        self.output_keep_prob = tf.placeholder(tf.float32, name="output_keep_prob")

        # embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            if self.config.embedding_type == EmbeddingType.word2vec:
                logging.info("Init embedding with word vector. (%d,%d)",
                             transformer.word_vector.shape[0], transformer.word_vector.shape[1])
                embedding_initializer = tf.constant_initializer(transformer.word_vector)
            else:
                logging.info("Init embedding with xavier initializer.")
                embedding_initializer = tf.contrib.layers.xavier_initializer()
            self._W = tf.get_variable("W", shape=[transformer.vocab_size, config.embedding_size],
                                      initializer=embedding_initializer,
                                      dtype=tf.float32)
            inputs = tf.nn.embedding_lookup(self._W, self.input)
            output_prev_inputs = tf.nn.embedding_lookup(self._W, self.output_prev_input)
            output_post_inputs = tf.nn.embedding_lookup(self._W, self.output_post_input)

        # encoder构建
        final_state = self.build_encoder(inputs, self.input_lengths)
        self.doc_vector = final_state

        # 前一句decoder
        prev_logits, self.prev_prediction, self.prev_state = self.build_decoder(output_prev_inputs,
                                                                                self.output_prev_lengths,
                                                                                final_state,
                                                                                name='prev_prediction')
        prev_loss = self.build_loss(prev_logits, self.output_prev_target, scope='prev_loss')

        # 后一句decoder
        post_logits, self.post_prediction, self.post_state = self.build_decoder(output_post_inputs,
                                                                                self.output_post_lengths,
                                                                                final_state,
                                                                                name='post_prediction')
        post_loss = self.build_loss(post_logits, self.output_post_target, scope='post_loss')

        with tf.variable_scope("loss"):
            self.loss = tf.add(prev_loss, post_loss, name="loss")

    def build_encoder(self, encode_emb, length):
        with tf.variable_scope('encoder'):
            cell = tf.nn.rnn_cell.GRUCell(num_units=self.config.hidden_size)
            cell = tf.contrib.rnn.DropoutWrapper(cell=cell, input_keep_prob=self.input_keep_prob)
            _, final_state = tf.nn.dynamic_rnn(cell, encode_emb, dtype=tf.float32, sequence_length=length)
        return final_state

    def build_decoder(self, decode_emb, length, state, name=''):
        with tf.variable_scope("decoder_" + name):
            cell = tf.nn.rnn_cell.GRUCell(num_units=self.config.hidden_size)
            cell = tf.contrib.rnn.DropoutWrapper(cell=cell, output_keep_prob=self.output_keep_prob)
            outputs, final_state = tf.nn.dynamic_rnn(cell, decode_emb, initial_state=state, sequence_length=length)
            x = tf.reshape(outputs, [-1, self.config.hidden_size])

        with tf.variable_scope('softmax_' + name):
            w = tf.get_variable("w", [self.config.hidden_size, self.transformer.vocab_size])
            b = tf.get_variable("b", [self.transformer.vocab_size])
            logits = tf.matmul(x, w) + b
            prediction = tf.nn.softmax(logits, name=name)
        return logits, prediction, final_state

    def build_loss(self, logits, targets, scope='loss'):
        with tf.variable_scope(scope):
            y_one_hot = tf.one_hot(targets, self.transformer.vocab_size)
            y_reshaped = tf.reshape(y_one_hot, [-1, self.transformer.vocab_size])
            loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y_reshaped))
        return loss

    def save(self, output_path):
        save_graph_value_scopes = [
            "loss/loss",
            self.doc_vector.name.split(":")[0],
            self.prev_prediction.name.split(":")[0],
            self.prev_state.name.split(":")[0],
            self.post_prediction.name.split(":")[0],
            self.post_state.name.split(":")[0],
        ]
        logging.info(save_graph_value_scopes)
        graph = tf.graph_util.convert_variables_to_constants(self.session, self.session.graph_def, save_graph_value_scopes)
        with tf.gfile.GFile(output_path+".pb", "wb") as f:
            f.write(graph.SerializeToString())

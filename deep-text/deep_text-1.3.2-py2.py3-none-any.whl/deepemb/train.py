# -*- coding=utf-8 -*-

from common.train import Trainer
from .skip_thought import SkipThought
import logging


class SkipThoughtTrainer(Trainer):
    def __init__(self, config, _transform_class, need_transform=False, rebuild_word2vec=False,
                 restore_model=False, optimizer=None):
        super(SkipThoughtTrainer, self).__init__(config, _transform_class, SkipThought,
                                                 need_transform, rebuild_word2vec,
                                                 restore_model, optimizer)
        self.train_ops.append(self.model.prev_prediction, self.model.post_prediction)

    def train_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["inputs"],
            self.model.input_lengths: batch_data["input_lens"],
            self.model.output_prev_input: batch_data["output_prevs"],
            self.model.output_prev_target: batch_data["target_prevs"],
            self.model.output_prev_lengths: batch_data["prev_lens"],
            self.model.output_post_input: batch_data["output_posts"],
            self.model.output_post_target: batch_data["target_posts"],
            self.model.output_post_lengths: batch_data["output_post_lens"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
        }

        _, step, summaries, loss, prev, post = self.session.run(self.train_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.train_summary_writer.add_summary(summaries, step)

    def dev_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["inputs"],
            self.model.input_lengths: batch_data["input_lens"],
            self.model.output_prev_input: batch_data["output_prevs"],
            self.model.output_prev_target: batch_data["target_prevs"],
            self.model.output_prev_lengths: batch_data["prev_lens"],
            self.model.output_post_input: batch_data["output_posts"],
            self.model.output_post_target: batch_data["target_posts"],
            self.model.output_post_lengths: batch_data["output_post_lens"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
        }

        step, summaries, loss = self.session.run(self.dev_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.dev_summary_writer.add_summary(summaries, step)


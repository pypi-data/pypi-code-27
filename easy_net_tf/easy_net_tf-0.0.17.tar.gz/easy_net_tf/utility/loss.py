import tensorflow as tf


class UtilityLoss:
    @staticmethod
    def cross_entropy_loss(prediction,
                           truth,
                           selections,
                           keep_ratio,
                           name,
                           debug=False):
        """

        :param prediction:
        :param truth: ground truth category. int32, int64 only
        :param selections: a list of selected categories.
        :param keep_ratio: keep top high 0.7 of cross entropy.
        :param name: a name for tf.summary
        :param debug: True: return loss,
                            valid_index,
                            raw_cross_entropy,
                            valid_cross_entropy,
                            top_cross_entropy;
                      False: return loss
        :return:
        """

        selection_0 = selections.pop(0)

        """
        valid index
        """
        valid_index = tf.equal(truth, selection_0)

        for valid_category in selections:
            valid_index = tf.logical_or(
                valid_index,
                tf.equal(truth, valid_category)
            )

        valid_total = tf.reduce_sum(
            tf.cast(
                valid_index,
                dtype=tf.float32)
        )

        mask_b = tf.multiply(
            tf.ones_like(truth),
            selection_0
        )
        truth = tf.cast(
            tf.where(
                valid_index,
                truth,
                mask_b
            ),
            tf.int32
        )

        """
        cross entropy
        """
        raw_cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=truth,
            logits=prediction
        )

        mask_0 = tf.zeros_like(raw_cross_entropy)

        valid_cross_entropy = tf.where(
            valid_index,
            raw_cross_entropy,
            mask_0
        )

        """
        keep ratio
        """
        keep_number = tf.cast(
            keep_ratio * valid_total,
            dtype=tf.int32
        )

        top_cross_entropy, _ = tf.nn.top_k(valid_cross_entropy, k=keep_number)

        """
        loss
        """
        loss = tf.reduce_mean(top_cross_entropy)

        tf.summary.scalar(name=name,
                          tensor=loss)

        if debug:
            return loss, valid_index, raw_cross_entropy, valid_cross_entropy, top_cross_entropy
        else:
            return loss

    @staticmethod
    def l2_loss(prediction,
                truth,
                categories,
                selections,
                keep_ratio,
                name,
                debug=False):
        """

        :param prediction:
        :param truth:
        :param categories: category label for each sample
        :param selections: a list of selected categories.
        :param keep_ratio: keep top high 0.7 of square error.
        :param name: a name for tf.summary
        :param debug: True: return loss,
                            valid_index,
                            raw_square_error,
                            valid_square_error,
                            top_square_error;
                      False: return loss
        :return:
        """

        selection_0 = selections.pop(0)

        """
        valid index
        """
        valid_index = tf.equal(categories, selection_0)

        for selection in selections:
            valid_index = tf.logical_or(
                valid_index,
                tf.equal(categories, selection)
            )

        valid_total = tf.reduce_sum(
            tf.cast(
                valid_index,
                dtype=tf.float32)
        )

        """
        square error
        """
        raw_square_error = tf.reduce_sum(
            tf.square(prediction - truth),
            axis=1
        )

        mask_0 = tf.zeros_like(raw_square_error)
        valid_square_error = tf.where(
            valid_index,
            raw_square_error,
            mask_0
        )

        """
        keep ratio
        """
        keep_num = tf.cast(
            keep_ratio * valid_total,
            dtype=tf.int32
        )

        top_square_error, _ = tf.nn.top_k(valid_square_error, k=keep_num)

        """
        loss
        """
        loss = tf.reduce_mean(top_square_error)

        tf.summary.scalar(name=name,
                          tensor=loss)

        if debug:
            return loss, valid_index, raw_square_error, valid_square_error, top_square_error
        else:
            return loss


if __name__ == '__main__':
    from easydict import EasyDict
    import numpy

    predicted = EasyDict()
    predicted.category = numpy.array([[0.9, 0.1],
                                      [0.8, 0.2],
                                      [0.7, 0.3],
                                      [0.6, 0.4],
                                      [0.5, 0.5],
                                      [0.4, 0.6],
                                      [0.3, 0.7],
                                      [0.2, 0.8],
                                      [0.1, 0.9]])
    predicted.offset = numpy.array([[0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1],
                                    [0.1, 0.1, 0.1, 0.1]])

    ground_truth = EasyDict()
    ground_truth.category = numpy.array([1,
                                         2,
                                         3,
                                         1,
                                         2,
                                         1,
                                         0,
                                         2,
                                         0])
    ground_truth.offset = numpy.array([[0.0, 0.1, 0.1, 0.1],
                                       [0.0, 0.0, 0.1, 0.1],
                                       [0.0, 0.0, 0.0, 0.1],
                                       [0.0, 0.0, 0.0, 0.0],
                                       [0.3, 0.1, 0.1, 0.1],
                                       [0.3, 0.3, 0.1, 0.1],
                                       [0.3, 0.3, 0.3, 0.1],
                                       [0.3, 0.3, 0.3, 0.3],
                                       [0.1, 0.5, 0.1, 0.1]])

    cross_entropy_op = UtilityLoss.cross_entropy_loss(prediction=predicted.category,
                                                      truth=ground_truth.category,
                                                      selections=[0, 1],
                                                      keep_ratio=0.8,
                                                      name='category',
                                                      debug=True)

    offset_loss_op = UtilityLoss.l2_loss(prediction=predicted.offset,
                                         truth=ground_truth.offset,
                                         categories=ground_truth.category,
                                         selections=[2],
                                         keep_ratio=1,
                                         name='offset',
                                         debug=True)

    with tf.Session() as sess:
        cross_entropy_ = sess.run(cross_entropy_op)
        offset_loss_ = sess.run(offset_loss_op)

        print(cross_entropy_)
        print(offset_loss_)

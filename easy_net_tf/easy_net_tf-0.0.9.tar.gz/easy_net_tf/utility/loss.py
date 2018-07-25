import tensorflow as tf


class UtilityLoss:
    @staticmethod
    def cross_entropy(prediction,
                      truth,
                      category_number,
                      keep_ratio,
                      name):
        """
        only category >= 0 be counted
        :param prediction:
        :param truth: ground truth category.
        :param category_number: category number.
        :param keep_ratio: keep top of 0.7 of example.
        :param name: a name for tf.summary
        :return:
        """

        zeros = tf.zeros_like(truth)
        ones = tf.ones_like(truth)

        # count total valid
        valid_index = tf.greater_equal(truth, 0)
        valid_total = tf.reduce_sum(
            tf.where(
                valid_index,
                ones,
                zeros)
        )

        # get one hot
        truth = tf.cast(
            tf.where(
                valid_index,
                truth,
                zeros
            ),
            tf.int32
        )

        category_one_hot = tf.one_hot(
            truth,
            depth=category_number
        )

        # calculate cross entropy
        cross_entropy = -tf.reduce_sum(category_one_hot * tf.log(tf.clip_by_value(prediction,
                                                                                  1e-8,
                                                                                  1.0)),
                                       axis=1)

        cross_entropy = tf.where(valid_index, cross_entropy, zeros)
        keep_num = tf.cast(keep_ratio * valid_total, tf.int32)
        cross_entropy, _ = tf.nn.top_k(cross_entropy, k=keep_num)

        loss = tf.reduce_mean(cross_entropy)

        tf.summary.scalar(name=name,
                          tensor=loss)
        return loss

    @staticmethod
    def regression(prediction,
                   truth,
                   categories,
                   selected,
                   name):
        """

        :param prediction:
        :param truth:
        :param categories: category label for each sample
        :param selected: selected category
        :param name: a name for tf.summary
        :return:
        """
        ones = tf.ones_like(categories)
        zeros = tf.zeros_like(categories)

        valid_index = tf.equal(categories, selected)
        valid_total = tf.reduce_sum(
            tf.where(valid_index, ones, zeros)
        )

        square_error = tf.reduce_sum(
            tf.square(prediction - truth),
            axis=1
        )

        square_error = tf.where(valid_index, square_error, zeros)

        loss = tf.reduce_sum(square_error) / valid_total

        tf.summary.scalar(name=name,
                          tensor=loss)

        return loss

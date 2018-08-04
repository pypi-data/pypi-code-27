from .utils import shuffled
import tensorflow as tf
import logging


class DecomposedTensor:
    """
    Represent CP / Tucker decomposition of a tensor in TensorFlow.

    """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def init_random(self, a=0.0, b=1.0):
        pass

    def init_components(self):
        pass

    def init_norm(self):
        pass

    def get_train_ops(self, X_var, optimizer):
        pass

    def get_fit_op(self, X, Y):
        """
        Squared frobenius norm operator of 2 tf.Variable
            ||X - Y||_F^2  = <X,X> + <Y,Y> - 2 <X,Y>

        """
        normX = tf.norm(X)**2
        normresidual = tf.norm(X - Y)**2
        return tf.constant(1., dtype=self.dtype) - normresidual / normX

    def train_als(self, X_data, optimizer, epochs=1000):
        """
        Use alt. least-squares to find the CP/Tucker decomposition of tensor `X`.

        """
        X_var = tf.Variable(X_data)
        loss_op, train_ops = self.get_train_ops(X_var, optimizer)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for e in range(epochs):
                for alt, train_op in enumerate(shuffled(train_ops)):
                    _, loss = sess.run(
                        [train_op, loss_op], feed_dict={X_var: X_data})
                    self.logger.debug('[%3d:%3d] loss: %.5f' % (e, alt, loss))

            self.logger.info('final loss: %.5f' % loss)
            return sess.run(self.X)

    def train_als_early(self,
                        X_data,
                        optimizer,
                        epochs=1000,
                        stop_freq=100,
                        stop_threshold=1e-10):
        """
        ALS with early stopping.

        """
        X_var = tf.Variable(X_data)
        loss_op, train_ops = self.get_train_ops(X_var, optimizer)
        fit_op = self.get_fit_op(X_var, self.X)
        fit_prev = 0.0

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for e in range(epochs):
                for alt, train_op in enumerate(shuffled(train_ops)):
                    _, loss = sess.run(
                        [train_op, loss_op], feed_dict={X_var: X_data})
                    self.logger.debug('[%3d:%3d] loss: %.5f' % (e, alt, loss))

                if stop_freq and e % stop_freq == 0:
                    fit = sess.run(fit_op)
                    fit_change = abs(fit - fit_prev)
                    if fit_change < stop_threshold:
                        self.logger.info(
                            'Early stop with fit_change: %.10f' % fit_change)
                        break
                    fit_prev = fit

            self.logger.info('final loss: %.5f' % loss)
            if stop_freq:
                self.logger.info('final fit %.5f' % fit)
            return sess.run(self.X)

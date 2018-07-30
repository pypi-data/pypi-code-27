import tensorflow as tf
import numpy as np
import functools

from hashlib import sha256
import os

CACHE_DIR = '__testdumps__'


class TestData(object):
    """Adds an additional `test_data` parameter to a given function.

  Test values are extracted from a TensorFlow computational graph
  instantiated from a checkpoint.

  Args:
    tf_checkpoint_dir (str): Path to the TensorFlow model checkpoint
      directory.
    tf_values (dict): Dictionary with arbitrary keys and values
      specifying graph nodes the output of which is dumped.
      The function that is wrapped will receive this dictionary
      as a `test_data` parameter, with keys unchanged and values
      being output tensors contained in NumPy arrays.
  """

    def __init__(self, tf_checkpoint_dir, tf_values):
        output_node_names = list(tf_values.values())
        outputs = compute_outputs_with_cache(
            tf_checkpoint_dir, output_node_names)

        self.test_data = {
            output_name: outputs[output_node_name]
            for (output_name, output_node_name) in tf_values.items()
        }

    def __call__(self, test_fn):
        @functools.wraps(test_fn)
        def with_inputs(*args, **kwargs):
            kwargs['test_data'] = self.test_data
            return test_fn(*args, **kwargs)

        return with_inputs


# TensorFlow utils


def load_graph_from_checkpoint(sess, chkpt_dir):
    latest_chkpt = tf.train.latest_checkpoint(chkpt_dir)
    assert latest_chkpt is not None, f'Unable to find a checkpoint in {chkpt_dir}'

    saver = tf.train.import_meta_graph(f'{latest_chkpt}.meta')
    saver.restore(sess, latest_chkpt)


def run_model_and_extract(sess, inputs, output_node_names):
    outputs = [
        tf.get_default_graph().get_tensor_by_name(n) for n in output_node_names
    ]
    return sess.run(outputs, inputs)


def random_inputs(sess):
    input_tensor_names = [
        f'{str(v, "utf8")}:0'
        for v in sess.run(tf.report_uninitialized_variables())
    ]
    return {
        input_name: sess.run(
            tf.random_uniform(
                tf.get_default_graph().get_tensor_by_name(input_name).shape))
        for input_name in input_tensor_names
    }


# Test value caching


def compute_outputs_with_cache(checkpoint_dir, node_names):
    restored = restore_cached(checkpoint_dir, node_names)
    cache_misses = [
        node_name for (node_name, tensor) in restored.items() if tensor is None
    ]

    if len(cache_misses) == 0:
        return restored

    tf.reset_default_graph()
    sess = tf.Session()

    load_graph_from_checkpoint(sess, checkpoint_dir)
    inputs = random_inputs(sess)
    output_values = run_model_and_extract(sess, inputs, cache_misses)

    computed = dict(zip(cache_misses, output_values))
    cache_outputs(checkpoint_dir, computed)

    return {**restored, **computed}


def cache_filename(checkpoint_dir, node_name):
    return sha256(
        f'{checkpoint_dir}//{node_name}'.encode('utf8')).hexdigest() + '.npy'


def restore_cached(checkpoint_dir, node_names):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cached_filenames = os.listdir(CACHE_DIR)

    nodes = [
        (node_name, cache_filename(checkpoint_dir, node_name))
        for node_name in node_names
    ]
    return {
        node_name: np.load(os.path.join(CACHE_DIR, cache_name))
        if cache_name in cached_filenames else None
        for (node_name, cache_name) in nodes
    }


def cache_outputs(checkpoint_dir, node_names_to_tensors):
    for (node_name, tensor) in node_names_to_tensors.items():
        np.save(
            os.path.join(CACHE_DIR, cache_filename(checkpoint_dir, node_name)),
            tensor)

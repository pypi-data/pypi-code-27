import numpy as np

def get_by_condition(preds, truths, confidences, condition):
    indices = np.where(condition(preds, truths))
    indexed_confidences = confidences[indices]
    return indexed_confidences


def get_incorrect_confidences(preds, truths, confidences):
    return get_by_condition(preds,truths, confidences, np.not_equal)

def  get_correct_confidences(preds, truths, confidences):
    return get_by_condition(preds, truths, confidences, np.equal)
import numpy as np

def rule_classifier_tfidf(X):
    # Hardcode
    POS_RULE1 = 147
    POS_RULE2 = 995
    POS_RULE3 = 884
    POS_RULE4 = 408

    rule_1 = X[:, POS_RULE1] > 1e-4
    rule_2 = X[:, POS_RULE2] > 1e-4
    rule_3 = X[:, POS_RULE3] > 1e-4
    rule_4 = X[:, POS_RULE4] > 1e-4

    temp_1 = np.bitwise_or(rule_1, rule_2)
    temp_2 = np.bitwise_or(temp_1, rule_3)
    temp_3 = np.bitwise_or(temp_2, rule_4)
    preds = temp_3.astype('int')
    return preds

def inverse_sigmoid(y):
    x = np.log(y/(1-y))
    return x
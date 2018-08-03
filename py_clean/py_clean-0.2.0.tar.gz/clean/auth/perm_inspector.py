from typing import Dict, Any


def get_value_from_dict(src: Dict, path: str, delimiter='.'):
    paths = path.split(delimiter)
    current = src
    for p in paths:
        if p in current:
            current = current[p]
        else:
            raise TypeError('{} not found in {}'.format(p, src))
    return current


def matcher_evaluator(operation: str, op_set: Dict, value: Any, expected: Any):
    func = op_set.get(operation)
    if callable(func) is False:
        raise TypeError('op_set <{}> is not callable'.format(func))
    return func(value, expected)


def match_in(value, expected):
    return expected in value


def match_eq(value, expected):
    return value == expected


OP_SET = {
    'in': match_in,
    'eq': match_eq
}


class PermissionInspector:

    class Meta:
        MATCHER_EVALUATOR = matcher_evaluator
        OP_SET = OP_SET

    def __init__(self, user: Dict = None, rule: Dict = None, allow_super: bool = False):
        self.user_type = {} if user is None else user
        self.rule = {} if rule is None else rule
        self.allow_super = allow_super

    def verify(self, token: Dict):
        try:
            return self.evaluate(token)
        except TypeError:
            return False

    def evaluate(self, token):
        user_req = self.user_type.get('req')
        user = self.get_user_type(token)
        if self.allow_super and user == 'admin':
            return True
        elif len(self.rule) == 0:
            return user_req == user
        else:
            value = get_value_from_dict(token, self.rule.get('path', ''))
            operation = self.rule.get('op', 'in')
            expected = self.rule.get('value')
            result = PermissionInspector.Meta.MATCHER_EVALUATOR(operation, self.Meta.OP_SET, value, expected)
            if user_req is user and result is True:
                return True
        return False

    @staticmethod
    def get_user_type(token: Dict):
        is_staff = token.get('staff', False)
        is_admin = token.get('admin', False)
        is_special = token.get('special', 0)
        if is_admin:
            return 'admin'
        if is_staff:
            return 'staff'
        if is_special:
            return is_special
        else:
            return 'user'

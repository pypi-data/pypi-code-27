from functools import wraps

from flask import abort, request


def validate_common(
        key_type_mapping: dict,
        code_when_content_type_is_not_json=406,
        key_missing_code=400,
        invalid_type_code=400):

    def validate_key_and_type(src, mapping):
        for key, typ in mapping.items():
            if key not in src:
                # 전형적인 bad request
                abort(key_missing_code)

            if type(typ) is dict:
                # int, str 등 type의 인스턴스가 와야 하는 자리에 {}(딕셔너리)가 전달된 경우(nested dict)
                validate_key_and_type(src[key], typ)
                # 명시된 key에 대해 validation을 재귀로 돌리도록
            elif type(src[key]) is not typ:
                abort(invalid_type_code)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(code_when_content_type_is_not_json)

            validate_key_and_type(request.json, key_type_mapping)

            return fn(*args, **kwargs)
        return wrapper
    return decorator

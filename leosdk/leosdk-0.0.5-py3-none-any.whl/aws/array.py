class Array:

    @staticmethod
    def merge(array1, array2):
        result = {}
        for key in array1:
            result[key] = array2[key] if key in array2 else array1[key]

        for key in array2:
            result[key] = result[key] if key in result else array2[key]

        return result

    @staticmethod
    def defaults(defaults, overrides):
        result = {}
        for key in defaults:
            result[key] = overrides[key] if key in overrides else defaults[key]

        return result

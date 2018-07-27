from builtins import object


class Photo(object):
    @classmethod
    def parse(cls, data):
        """
        Converts JSON structure into Photo object where
        each JSON key,value has become a Photo property

        :param data: json body of a single photo entry
        :return: Photo object
        """
        data = data or {}
        photo = cls() if data else None

        for key, value in data.items():
            setattr(photo, key, value)

        return photo

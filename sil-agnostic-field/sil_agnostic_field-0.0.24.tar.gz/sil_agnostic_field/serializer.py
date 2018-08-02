from rest_framework import serializers


class AgnosticField(serializers.Field):
    def to_representation(self, value):
        if (isinstance(value, list)):
            return value
        elif (isinstance(value, dict)):
            return value
        return None

    def to_internal_value(self, value):
        return value

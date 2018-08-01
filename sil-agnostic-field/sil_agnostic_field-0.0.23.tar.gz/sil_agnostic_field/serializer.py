from rest_framework import serializers

class AgnosticFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if (isinstance(value, list)):
            return value
        elif (isinstance(value),dict):
            return value
        return None
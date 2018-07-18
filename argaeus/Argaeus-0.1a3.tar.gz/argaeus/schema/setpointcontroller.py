def get_schema():
    schema = {
        "setpoint-controller": {
            "description": "changes the set-point of the current program",
            "type": "object",
            "properties": {
                "topic-sub-left": {
                    "description": "rotate left topic",
                    "type": "string"
                },
                "command-left": {
                    "description": "rotate left command - if this value is published to topic-sub-left, a rotation step"
                                   "to the left is assumed.",
                    "type": "string"
                },
                "topic-sub-right": {
                    "description": "rotate right topic",
                    "type": "string"
                },
                "command-right": {
                    "description": "rotate right command - if this value is published to topic-sub-left, a rotation "
                                   "step to the right is assumed.",
                    "type": "string"
                },
                "step-size": {
                    "description": "Temperature is changed by step size for each rotation step.",
                    "type": "number"
                },
                "max-temp": {
                    "description": "Maximum value for temperature",
                    "type": "number"
                },
                "min-temp": {
                    "description": "Minimum value for temperature",
                    "type": "number"
                },
            },
            "required": ["topic-sub-left", "command-left", "topic-sub-right", "command-right", "step-size",
                         "max-temp", "min-temp"],
            "additionalProperties": False
        }
    }

    return schema

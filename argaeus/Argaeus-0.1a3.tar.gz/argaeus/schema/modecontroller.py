import argaeus.schema.modeprogram
import argaeus.schema.modeschedule


def get_schema():
    schema = {
        "mode-controller": {
            "description": "list of different operation modes like fixed temperature or time schedule driven",
            "type": "object",
            "properties": {
                "default-mode": {
                    "description": "default mode - must be a name from modes list",
                    "type": "string"
                },
                "topics-pub": {
                    "description": "outgoing topics",
                    "type": "object",
                    "properties": {
                        "display-server-schedule-image": {
                            "description": "topic of an nikippe-mqttimage instance",
                            "type": "string"
                        },
                        "display-server-mode-icon": {
                            "description": "topic of an nikippe-imagelist instance",
                            "type": "string"
                        },
                        "temperature-set-point": {
                            "description": "topic of e.g. epidaurus (=pid temperature control) set-point listener",
                            "type": "string"
                        },
                    },
                    "required": ["display-server-schedule-image", "display-server-mode-icon", "temperature-set-point"],
                    "additionalItems": False
                },
                "topics-sub": {
                    "description": "incoming topics",
                    "type": "object",
                    "properties": {
                        "to-left": {
                            "description": "rotate left topic",
                            "type": "string"
                        },
                        "command-left": {
                            "description": "rotate left command - if this value is published to topic-sub-left, a rotation step"
                                           "to the left is assumed.",
                            "type": "string"
                        },
                        "to-right": {
                            "description": "rotate right topic",
                            "type": "string"
                        },
                        "command-right": {
                            "description": "rotate right command - if this value is published to topic-sub-left, a rotation "
                                           "step to the right is assumed.",
                            "type": "string"
                        },
                    },
                    "required": ["to-left", "command-left", "to-right", "command-right"],
                    "additionalItems": False
                },
                "modes": {
                    "description": "list of modes",
                    "type": "array",
                    "items": {
                        "anyof": [
                            argaeus.schema.modeschedule.get_schema(),
                            argaeus.schema.modeprogram.get_schema()
                        ]
                    }
                },

            },
            "required": ["default-mode", "topics-sub", "topics-pub", "modes"],
            "additionalProperties": False
        }
    }

    return schema

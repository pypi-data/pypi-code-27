def get_schema():
    schema = {
        "button-controller": {
            "description": "maps incoming events from buttons to internal events",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "description": "unique name for mapping entry",
                        "type": "string"
                    },
                    "topic-sub": {
                        "description": "incoming events",
                        "type": "string"
                    },
                    "command-active": {
                        "description": "event is detected if this command is received via topic-sub.",
                        "type": "string"
                    },
                    "behavior": {
                        "description": "possible internal events",
                        "type": "string",
                        "enum": ["to-default-mode", "toggle-active-passive", "reset-to-default-temp"]
                    }
                },
                "required": ["name", "topic-sub", "command-active", "behavior"],
                "additionalItems": False
            },
            "additionalItems": False
        }
    }

    return schema

from functools import wraps

events = []

def add_channel(*args, **kwargs):
    pusher_data = {}

    if args and type(args[0]) == str:
        pusher_data['channel_name'] = args[0]
    
    for key, value in kwargs.items():
        if key not in pusher_data:
            pusher_data[key] = value
    
    if 'channel_name' not in pusher_data:
        raise TypeError('add_channel() missing 1 required positional argument: \'channel_name\'')

    
    def wrapper(function):

        @wraps(function)
        def _wrapper():
            if 'event_name' not in pusher_data:
                pusher_data['event_name'] = function.__name__


            events.append(
                {
                    'channel_name': pusher_data['channel_name'],
                    'event_name': pusher_data['event_name'],
                    'function': function,
                }
            )

        return _wrapper()

    return wrapper
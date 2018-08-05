class SampleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("__init__")

    def __call__(self, request):
        print('__before_response__')

        response = self.get_response(request)

        print('__after_response__')

        return response

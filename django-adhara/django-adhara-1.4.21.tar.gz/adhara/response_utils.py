from django.http import JsonResponse


class ApiResponse:

    class Pratikriyaa(JsonResponse):
        """
        Error Response Class
        """
        pass

    class SkhalitaPratikriyaa(JsonResponse):
        """
        Error Response Class
        """
        status_code = 400

        def __init__(self, data, **kwargs):
            super(ApiResponse.SkhalitaPratikriyaa, self).__init__(data, safe=False, **kwargs)

    class AsiddhauPratikriyaa(JsonResponse):
        """
        Failure Response Class
        """
        status_code = 500

        def __init__(self, data, **kwargs):
            super(ApiResponse.AsiddhauPratikriyaa, self).__init__(data, safe=False, **kwargs)

    class NotAllowedPratikriyaa(JsonResponse):
        """
            Failure Response Class
        """
        status_code = 405

        def __init__(self, data, **kwargs):
            super(ApiResponse.NotAllowedPratikriyaa, self).__init__(data, safe=False, **kwargs)

    class NiSiddhaPratikriyaa(JsonResponse):
        """
            Forbidden Response Class
        """
        status_code = 403

        def __init__(self, data, **kwargs):
            super(ApiResponse.NiSiddhaPratikriyaa, self).__init__(data, safe=False, **kwargs)

    @staticmethod
    def success(data=None, meta=None):
        pratikriyaa = {
            "status": "success",
            "data": data
        }
        if meta is not None:
            pratikriyaa["meta"] = meta
        return ApiResponse.Pratikriyaa(pratikriyaa)

    @staticmethod
    def error(message):
        pratikriyaa = {
            "status": "error",
            "data": message
        }
        return ApiResponse.SkhalitaPratikriyaa(pratikriyaa)

    @staticmethod
    def failure(failures):
        pratikriyaa = {
            "status": "failure",
            "data": failures
        }
        return ApiResponse.AsiddhauPratikriyaa(pratikriyaa)

    @staticmethod
    def forbidden(message):
        pratikriyaa = {
            "status": "forbidden",
            "data": message
        }
        return ApiResponse.NiSiddhaPratikriyaa(pratikriyaa)

    @staticmethod
    def respond(data, status="success", status_code=200):
        _status_code = status_code

        class Pratikriyaa(JsonResponse):
            status_code = _status_code

            def __init__(self, _data, **kwargs):
                super(Pratikriyaa, self).__init__(_data, safe=False, **kwargs)

        Pratikriyaa({
            "status": status,
            "data": data
        })

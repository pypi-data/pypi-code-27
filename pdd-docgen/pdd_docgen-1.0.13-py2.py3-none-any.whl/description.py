class Description:
    def __init__(
            self, name, introduction, hide_headers=[], extra_curl_params=[]):
        self.name = name
        self.introduction = introduction
        self.hide_headers = hide_headers
        self.extra_curl_params = extra_curl_params

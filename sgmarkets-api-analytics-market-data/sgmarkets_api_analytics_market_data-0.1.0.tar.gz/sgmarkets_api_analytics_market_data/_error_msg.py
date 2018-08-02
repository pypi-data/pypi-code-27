class Error:
    def Msg(N=0):
        assert isinstance(N, int), \
            'Error N must be an int'

        error = ['Error: li_raw_data must be a list - Run call_api() again with debug=True',
                 ]
        return error[N]

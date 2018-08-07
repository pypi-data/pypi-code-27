import requests, json

class OreumUMS:
    BASE_URI = 'https://api.smsrang.co.kr'

    def __init__(self, seckey):
        self.seckey = seckey
        self.send = None
        self.recv = None
        self.msg = None
        self.subject = None

    def _check_args(self):
        no_args = []
        if not self.seckey:
            no_args.append('seckey')
        if not self.send:
            no_args.append('send')
        if not self.recv:
            no_args.append('recv')
        if not self.msg:
            no_args.append('msg')

        if no_args:
            print('No arguments: %s' % ', '.join(no_args))
            return False

        return True

    def send_sms(self, obj={}):
        if 'send' in obj:
            self.send = obj['send']
        if 'recv' in obj:
            self.recv = obj['recv']
        if 'msg' in obj:
            self.msg = obj['msg']

        if not self._check_args():
            return False, 'No arguments'

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'OREUM-SECRET-KEY': self.seckey
        }

        data = {
            'tr_callback': self.send.replace('-', ''),
            'tr_phone': self.recv.replace('-', ''),
            'tr_msg': self.msg
        }

        res = requests.post(self.BASE_URI + '/sms',
            headers=headers,
            data=json.dumps(data))

        if res.status_code == 500:
            return False, 'Server error'
        elif res.status_code != 201:
            return False, res.json()['detail']

        return True, ''

    def send_sms_multiple(self, obj={}):
        if 'send' in obj:
            self.send = obj['send']
        if 'recv' in obj:
            if type(obj['recv']) == list:
                self.recv = ','.join(obj['recv'])
            else:
                self.recv = obj['recv']
        if 'msg' in obj:
            self.msg = obj['msg']

        if not self._check_args():
            return False, 'No arguments'

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'OREUM-SECRET-KEY': self.seckey
        }

        data = {
            'tr_callback': self.send.replace('-', ''),
            'tr_phones': self.recv.replace('-', ''),
            'tr_msg': self.msg
        }

        res = requests.post(self.BASE_URI + '/sms/multiple',
            headers=headers,
            data=json.dumps(data))

        if res.status_code == 500:
            return False, 'Server error'
        elif res.status_code != 201:
            return False, res.json()['detail']

        return True, ''
    def send_mms(self, obj={}):
        if 'send' in obj:
            self.send = obj['send']
        if 'recv' in obj:
            self.recv = obj['recv']
        if 'msg' in obj:
            self.msg = obj['msg']
        if 'subject' in obj:
            self.subject = obj['subject']

        if not self._check_args():
            return False, 'No arguments'

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'OREUM-SECRET-KEY': self.seckey
        }

        data = {
            'callback': self.send.replace('-', ''),
            'phone': self.recv.replace('-', ''),
            'msg': self.msg,
            'subject': self.subject
        }

        res = requests.post(self.BASE_URI + '/mms',
            headers=headers,
            data=json.dumps(data))

        if res.status_code == 500:
            return False, 'Server error'
        elif res.status_code != 201:
            return False, res.json()['detail']

        return True, ''

    def send_mms_multiple(self, obj={}):
        if 'send' in obj:
            self.send = obj['send']
        if 'recv' in obj:
            if type(obj['recv']) == list:
                self.recv = ','.join(obj['recv'])
            else:
                self.recv = obj['recv']
        if 'msg' in obj:
            self.msg = obj['msg']
        if 'subject' in obj:
            self.subject = obj['subject']

        if not self._check_args():
            return False, 'No arguments'

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'OREUM-SECRET-KEY': self.seckey
        }

        data = {
            'callback': self.send.replace('-', ''),
            'phones': self.recv.replace('-', ''),
            'msg': self.msg,
            'subject': self.subject
        }

        res = requests.post(self.BASE_URI + '/mms/multiple',
            headers=headers,
            data=json.dumps(data))

        if res.status_code == 500:
            return False, 'Server error'
        elif res.status_code != 201:
            return False, res.json()['detail']

        return True, ''

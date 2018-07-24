import requests

from .server import get_url

def send_task(taskType, data):
    data['task'] = taskType
    response = requests.post(get_url() + '/task', json=data).json()
    if 'id' in response.keys():
        return response['id']
    else:
        print('An error happened: server did not respond')
        return None

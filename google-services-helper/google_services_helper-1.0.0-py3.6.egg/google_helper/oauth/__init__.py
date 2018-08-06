from .authorization_helper import Authorizer

'''
usage is like fallows:

from oauth import Authorizer

authorizer = Authorizer(client_secret_path='path/to/client_secret.json', credentials_storage_path='path/to/credentials.json', scopes=['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly'])

authorizer.authorize()
'''


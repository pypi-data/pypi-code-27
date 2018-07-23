from __future__ import print_function
import csv
from dash_auth import Register, AccountApi
from dash_api import UserApi, User as UserModel
from dash_auth.rest import ApiException as AuthApiException
from dash_api.rest import ApiException as AppApiException


class User(object):

    def __init__(self, client_factory):
        self.client_factory = client_factory

    def import_from_file(self, file):
        reader = csv.DictReader(file)
        for row in reader:
            register = Register()
            register.first_name = row['firstName']
            register.surname = row['surname']
            register.email = row['email']
            register.gender = row['gender']
            register.address = row['address']
            register.suburb = row['suburb']
            register.state = row['state']
            register.mobile_phone_number = row['mobilePhoneNumber']
            register.password = row['password']
            register.postcode = row['postcode']

            print('Importing user {email}'.format(email=register.email))
            response = self.get_user(register.email)
            if len(response) > 0:
                provider_id = response[0].subject
                self.check_add_user_to_app(provider_id)
                print('User {email} imported'.format(email=register.email))
            else:
                added = self.add_user_auth(register)
                if added == True:
                    response = self.get_user(register.email)
                    provider_id = response[0].subject
                    self.check_add_user_to_app(provider_id)
                    print('User {email} imported'.format(email=register.email))
                else:
                    print('Failed to import {email}'.format(email=register.email))

    def check_add_user_to_app(self, subject):
        user_exists = self.check_user_in_app(subject)
        if user_exists == False:
            user = UserModel()
            user.provider_id = subject
            self.add_user_app(user)
        else:
            print('User exists - skipping')

    def get_user(self, email_address):
        auth_client = self.client_factory.get_auth_api_client()
        account_api = AccountApi(auth_client)
        try:
            response = account_api.api_account_get(email_addresses=[email_address])
            return response
        except AuthApiException:
            return []
    
    def add_user_auth(self, register):
        auth_client = self.client_factory.get_auth_api_client()
        account_api = AccountApi(auth_client)
        try:
            account_api.api_account_post(value=register)
            return True
        except AuthApiException as e:
            print(e)
            return False
    
    def add_user_app(self, user):
        app_client = self.client_factory.get_app_api_client()
        user_api = UserApi(app_client)
        try:
            response = user_api.api_user_post(model=user)
            return response
        except AppApiException as e:
            print(e)
            return None

    def check_user_in_app(self, provider_id):
        app_client = self.client_factory.get_app_api_client()
        user_api = UserApi(app_client)
        try:
            user_api.api_user_by_provider_id_head(provider_id)
            return True
        except AppApiException:
            return False
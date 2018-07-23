from __future__ import print_function
import csv
from dash_auth import AccountApi
from dash_api import UserApi, OrganisationApi, Organisation
from dash_auth.rest import ApiException as AuthApiException
from dash_api.rest import ApiException as AppApiException
from pprint import pprint

class UserOrg(object):

    def __init__(self, client_factory):
        self.client_factory = client_factory

    def import_from_file(self, file):
        reader = csv.DictReader(file)
        for row in reader:
            email_address = row['email']
            organisation_id = row['organisation_id']
            assignment = row['assignment']

            users = self.get_user_from_email(email_address)
            if len(users) > 0:
                org = self.get_organisation(organisation_id)
                if org is not None:
                    success = self.associate_user_with_org(users[0].provider_id,
                                                        assignment, org)
                    if success == True:
                        print('Association successful')
                    else:
                        print('Association failed')
                else:
                    print('Could not find organisation')
            else:
                print('Could not find user {email} - skipping'.format(email=email_address))

    
    def get_user_from_email(self, email_address):
        auth_client = self.client_factory.get_auth_api_client()
        account_api = AccountApi(auth_client)
        try:
            response = account_api.api_account_get(email_addresses=[email_address])
            return response
        except AuthApiException:
            return []

    def get_organisation(self, org_id):
        app_client = self.client_factory.get_app_api_client()
        org_api = OrganisationApi(app_client)
        try:
            response = org_api.api_organisation_by_id_get(org_id)
            return response
        except AppApiException as e:
            pprint(e)
            return None

    def associate_user_with_org(self, provider_id, assignment, organisation):
        app_client = self.client_factory.get_app_api_client()
        user_api = UserApi(app_client)
        try:
            user_api.api_user_by_provider_id_organisations_by_assignment_post(provider_id,
                assignment, organisation=organisation)
            return True
        except AppApiException as e:
            pprint(e)
            return False
        


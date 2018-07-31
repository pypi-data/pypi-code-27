from directory_client_core.base import BaseAPIClient

from directory_api_client.buyer import BuyerAPIClient
from directory_api_client.company import CompanyAPIClient
from directory_api_client.enrolment import EnrolmentAPIClient
from directory_api_client.supplier import SupplierAPIClient
from directory_api_client.notifications import NotificationsAPIClient
from directory_api_client.exportopportunity import ExportOpportunityAPIClient
from directory_api_client.exportreadiness import ExportReadinessAPIClient


class DirectoryAPIClient(BaseAPIClient):

    endpoints = {
        'ping': 'healthcheck/ping/',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enrolment = EnrolmentAPIClient(*args, **kwargs)
        self.company = CompanyAPIClient(*args, **kwargs)
        self.supplier = SupplierAPIClient(*args, **kwargs)
        self.buyer = BuyerAPIClient(*args, **kwargs)
        self.notifications = NotificationsAPIClient(*args, **kwargs)
        self.exportopportunity = ExportOpportunityAPIClient(*args, **kwargs)
        self.exportreadiness = ExportReadinessAPIClient(*args, **kwargs)

    def ping(self):
        return self.get(url=self.endpoints['ping'])

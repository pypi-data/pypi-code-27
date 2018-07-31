from apisdk.controller.ApiController import *
from cybersource_authentication_sdk_python.sample_code.Get_Generate_Headers import *
from authenticationsdk.util.PropertiesUtil import *


class GetObjectMethod:
    def __init__(self):

        # UNIQUE GET ID [EDITABLE]
        self.get_id = "5246387105766473203529"
        # REQUEST TARGET [EDITABLE]
        self.request_target = "/pts/v2/payments/" + self.get_id
        # REQUEST-TYPE [NOT-EDITABLE]
        self.request_type = "GET"
        # give the URL path to where the data needs to be authenticated
        self.url = GlobalLabelParameters.HTTP_URL_PREFIX

    def get_object_method(self):

        try:
            # Here we read the properties values from cybs.json.The dictionary (details dict 1) has all the details
            util_obj = PropertiesUtil()
            details_dict1 = util_obj.configarion()
            # Here we set the values from dictionary to Merchant Configaration object
            global mconfig
            mconfig = MerchantConfigaration()
            mconfig.set_merchantconfig(details_dict1)
            # This implements the fall back logic for JWT parameters key alias,key password,json file path
            mconfig.validate_merchant_details(details_dict1, mconfig)
            # Setting the url ,request_host_url,request_type to MerchantConfigaration object
            mconfig.request_type_method = self.request_type
            mconfig.request_target = self.request_target
            mconfig.url = self.url + mconfig.request_host + mconfig.request_target
            # Here we initiate the controller
            self.process()
        except ApiException as e:
            print(e)
        except IOError as e:
            print(GlobalLabelParameters.FILE_NOT_FOUND + str(e.filename))
        except KeyError as e:
            print(GlobalLabelParameters.NOT_ENTERED + str(e))
        except Exception as e:
            print(e)

    # noinspection PyMethodMayBeStatic
    def process(self):

        api_controller = ApiController()
        # This transfers the code to the API Controller
        api_controller.payment_get(mconfig)
        # Printing the Response Code,URL,V-C-Correlation-Id,Response message in the console
        print(" URL                : " + mconfig.url)
        print(" Response Code      : " + str(mconfig.response_code))
        print(" V-C-Corealation ID : " + mconfig.v_c_correlation_id)
        print(" Response Message   : " + mconfig.response_message)


if __name__ == "__main__":
    sample_obj = GetObjectMethod()
    sample_obj.get_object_method()

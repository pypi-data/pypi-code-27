from apisdk.controller.ApiController import *
from cybersource_authentication_sdk_python.sample_code.Post_Generate_Headers import *
from authenticationsdk.util.PropertiesUtil import *
import cybersource_authentication_sdk_python.data.RequestData
from authenticationsdk.core.ExceptionHandling import *


class PostMethod:
    def __init__(self):
        # REQUEST TARGET [EDITABLE]
        self.request_target = "/pts/v2/payments"
        # REQUEST-TYPE [NOT-EDITABLE]
        self.request_type = "POST"
        # REQUEST-JSON-PATH [NOT-EDITABLE]
        self.request_json_path = "../../cybersource_authentication_sdk_python/Resources/request.json"
        self.url = GlobalLabelParameters.HTTP_URL_PREFIX

    def post_method(self):

        try:
            # Here we read the properties values from cybs.json.The dictionary (details dict 1) has all the details
            util_obj = PropertiesUtil()
            details_dict1 = util_obj.properties_util()
            # Here we set the values from dictionary to Merchant Configaration object
            global mconfig
            mconfig = MerchantConfigaration()
            mconfig.set_merchantconfig(details_dict1)
            # This implements the fall back logic for JWT parameters key alias,key password,json file path
            mconfig.validate_merchant_details(details_dict1, mconfig)
            mconfig.request_json_path_data = cybersource_authentication_sdk_python.data.RequestData.json_file_data(
                self.request_json_path, mconfig)
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
            print(repr(e))

    # noinspection PyMethodMayBeStatic
    def process(self):

        api_controller = ApiController()
        # This transfers the code to the API Controller
        api_controller.payment_post(mconfig)
        # Printing the Response Code,URL,V-C-Correlation-Id,Response message in the console
        print(" URL                : " + mconfig.url)
        print(" Response Code      : " + str(mconfig.response_code))
        print(" Response Message   : " + mconfig.response_message)
        print(" V-C-Corealation ID : " + mconfig.v_c_correlation_id)


if __name__ == "__main__":
    sample_obj = PostMethod()

    sample_obj.post_method()

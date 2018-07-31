from authenticationsdk.core.Authorization import *
from authenticationsdk.core.MerchantConfigaration import *
import authenticationsdk.logger.Log
from authenticationsdk.util.PropertiesUtil import *
import authenticationsdk.util.ExceptionAuth


class DeleteGenerateHeaders:
    def __init__(self):
        # REQUEST TARGET [EDITABLE]
        self.request_target = "/reporting/v2/reportSubscriptions/TRRReport?organizationId=testrest"
        # REQUEST-TYPE [NOT-EDITABLE]
        self.request_type = "DELETE"
        self.merchant_config = None
        self.date = None

    def delete_generate_header(self):

        try:
            # Here we read the properties values from cybs.json.The dictionary (details dict 1) has all the details
            util_obj = PropertiesUtil()
            details_dict1 = util_obj.properties_util()
            # Here we set the values from dictionary to Merchant Configaration object
            mconfig = MerchantConfigaration()
            mconfig.set_merchantconfig(details_dict1)
            # This implements the fall back logic for JWT parameters key alias,key password,json file path
            mconfig.validate_merchant_details(details_dict1, mconfig)
            # Setting the url ,request_host_url,request_type to MerchantConfigaration object
            self.merchant_config = mconfig
            self.merchant_config.request_host = mconfig.request_host
            self.merchant_config.request_type_method = self.request_type
            mconfig.request_target = self.request_target
            self.date = mconfig.get_time()
            self.delete_method_headers()
        except ApiException as e:
            print(e)
        except KeyError as e:
            print(GlobalLabelParameters.NOT_ENTERED + str(e))
        except IOError as e:
            print(GlobalLabelParameters.FILE_NOT_FOUND + str(e.filename))

    # This method prints values obtained in our code by connecting to AUTH sdk
    def delete_method_headers(self):
        logger = self.merchant_config.log
        try:
            auth = Authorization()
            authentication_type = self.merchant_config.authentication_type
            print("Request Type    :" + self.request_type)
            print(GlobalLabelParameters.CONTENT_TYPE + "       :" + GlobalLabelParameters.APPLICATION_JSON)
            # This methods allow s to directly allow us to connect to AUTH SDK  depending on authentication type
            if authentication_type.upper() == GlobalLabelParameters.HTTP.upper():
                print(" " + GlobalLabelParameters.USER_AGENT + "          : " + GlobalLabelParameters.USER_AGENT_VALUE)
                print(" MerchantID          : " + self.merchant_config.merchant_id)
                print(" Date                : " + self.merchant_config.get_time())

                temp_sig = auth.get_token(self.merchant_config, self.date, logger)
                print("Signature Header      :" + str(temp_sig))
                print("Host                  :" + self.merchant_config.request_host)
            else:

                temp_sig = auth.get_token(self.merchant_config, self.date, logger)
                print("Authorization Bearer            :" + str(temp_sig))
            if self.merchant_config.enable_log is True:
                logger.info("END> ======================================= ")
                logger.info("\n")
        except ApiException as e:
            authenticationsdk.util.ExceptionAuth.log_exception(logger, e, self.merchant_config)
        except Exception as e:
            authenticationsdk.util.ExceptionAuth.log_exception(logger, repr(e), self.merchant_config)


if __name__ == "__main__":
    post_generate_obj = DeleteGenerateHeaders()
    post_generate_obj.delete_generate_header()

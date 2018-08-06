from consent_decoder.decoder.VendorConsentDecoder import *


def all(consentString):
    vendorDecoder = VendorConsentDecoder();
    vendorConsent = vendorDecoder.fromBase64String(consentString);
    return vendorDecoder.getVendor(vendorConsent);
     
    

def field(consentString, choice):
    vendorDecoder = VendorConsentDecoder();
    if int(choice) < 12  and int(choice) > 0:
            vendorConsent = vendorDecoder.fromBase64String(consentString);
            return vendorDecoder.getVendorRequiredField(vendorConsent, choice);
    else:
        print("Invalid choice " + str(choice) + "must be between 1 to 11")
 
    
if __name__ == "__main__":
    
   vendorDecoder = VendorConsentDecoder();
   totalArguments = len(sys.argv);
   
   try:
        if totalArguments == 2:
            consentString = sys.argv[1];
            vendorConsent =  vendorDecoder.fromBase64String(consentString);
            vendorDecoder.printAllVendorFields(vendorConsent);
        elif totalArguments == 3:
            consentString = sys.argv[1]
            choice = int(sys.argv[2]);

            if choice < 12  and choice > 0:
                vendorConsent =  vendorDecoder.fromBase64String(consentString);
                vendorDecoder.printVendorRequiredField(vendorConsent,choice);
            else:
                print("Invalid choice " + str(choice) + "must be between 1 to 11")
        else:
            vendorDecoder.usage();
            
   except Exception as ex:
        print("Exception Occurred {0}".format(str(ex.args[0])).encode("utf-8"))
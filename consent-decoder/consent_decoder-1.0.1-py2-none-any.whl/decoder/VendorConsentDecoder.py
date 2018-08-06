import base64
import sys
from consent_decoder.util.Bits import Bits
from consent_decoder.util.GdprConstants import GdprConstants
from consent_decoder.vendor.VendorConsent import VendorConsent
from consent_decoder.vendor import Vendor;

class VendorConsentDecoder:
    
    #--------validate consent string and decode to byte array
    
    def fromBase64String(self,consentString):
        if consentString:
            return self.fromByteArray(self.decodeString(consentString));
    
    #------- Get version of vendor from consent decoded string.
    
    def getVersion(self, bits):
        return bits.getInt(GdprConstants.VERSION_BIT_OFFSET, GdprConstants.VERSION_BIT_SIZE);

    #-----get Vendor Consent Object from decoded consent string 
    
    def fromByteArray(self, bytesArray):
        if bytes != None:
            bits = Bits(bytesArray);
            version = self.getVersion(bits);
            
            if version == 1:
                return VendorConsent(bits);
            else:
                raise ValueError('this' + str(version) + 'Not Supported')
         
    
    #------- this will decode the consent string base 64 encoded
    #------- and also add padding in case if string is not properly padded.
    
    def decodeString(self, value):
        if len(value) % 4 != 0: #check if multiple of 4
            while len(value) % 4 != 0:
                value = value + "="
            return bytearray(base64.urlsafe_b64decode(value));
        else:
            return bytearray(base64.urlsafe_b64decode(value));        
    
    def usage(self):
        print ("Usage " + sys.argv[0]+  " {consent string}") 
        
        print ("-----------OR --------------------") 
        print ("Usage " + sys.argv[0]+  " {consent string} {choice}")
        
        print ("1 : Version")   
        print ("2 : CMP ID (Consent Management Platform ID)")
        print ("3 : CMP Version (Consent Management Platform Version)")    
        print ("4 : Vendor List Version")   
        print ("5 : Allowed Purpose Ids")   
        print ("6 : Max Vendor Id")   
        print ("7 : Consent Record Created Date")   
        print ("8 : Consent Record Updated Date")   
        print ("9 : Consent Screen")
        print ("10 : Consent Language") 
        print ("11 : Allowed Vendor Ids") 
        
    
    def printAllVendorFields(self, vendorDecoder):
        
        print (vendorDecoder.getVersion());
        print (vendorDecoder.getCmpId());
        print (vendorDecoder.getVendorListVersion());
        print (vendorDecoder.getAllowedPurposeIds());
        print (vendorDecoder.getMaxVendorId());
        print (vendorDecoder.getConsentRecordCreated());
        print (vendorDecoder.getConsentRecordLastUpdated());
        print (vendorDecoder.getCmpVersion());
        print (vendorDecoder.getConsentScreen());
        print (vendorDecoder.getConsentLanguage());
        print (vendorDecoder.getAllowedVendorId());
    
    def getVendor(self, vendorDecoder):
        vendor = Vendor.Vendor();
         
        vendor.version = vendorDecoder.getVersion();
        vendor.cmpId =  vendorDecoder.getCmpId();
        vendor.cmpVersion = vendorDecoder.getCmpVersion();
        vendor.vendorListVersion = vendorDecoder.getVendorListVersion();
        vendor.allowedPurposeIds = vendorDecoder.getAllowedPurposeIds();
        vendor.maxVendorId = vendorDecoder.getMaxVendorId();
        vendor.recordCreatedDate = vendorDecoder.getConsentRecordCreated();
        vendor.recordUpdatedDate = vendorDecoder.getConsentRecordLastUpdated();
        vendor.consentScreen = vendorDecoder.getConsentScreen();
        vendor.consentLanguage = vendorDecoder.getConsentLanguage(); 
        vendor.allowedVendorIds = vendorDecoder.getAllowedVendorId();
         
        return vendor;
    
    
    def printVendorRequiredField(self,vendor, choice):
        print  self.getVendorRequiredField(vendor, choice)
     
    def getVendorRequiredField(self, vendor, choice):
         switcher = {
                1: vendor.getVersion,
                2: vendor.getCmpId,
                3: vendor.getCmpVersion,
                4: vendor.getVendorListVersion,
                5: vendor.getAllowedPurposeIds,
                6: vendor.getMaxVendorId,
                7: vendor.getConsentRecordCreated,
                8: vendor.getConsentRecordLastUpdated, 
                9: vendor.getConsentScreen,
                10: vendor.getConsentLanguage,
                11: vendor.getAllowedVendorId
            };
            
         func = switcher.get(choice, "nothing");    
         return (func());
    
        

         

   
    
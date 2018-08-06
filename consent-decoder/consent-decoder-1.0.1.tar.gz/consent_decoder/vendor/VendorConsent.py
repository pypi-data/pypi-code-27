from consent_decoder.util.Bits import Bits
from consent_decoder.util.GdprConstants import GdprConstants


class VendorConsent:
    
    Bits

    def __init__(self, Bits):
        self.Bits = Bits
    
    
    #-- get version of Vendor
    #--- Version is present between  0 and 6 bits of consent string   
    def getVersion(self):
        return self.Bits.getInt(GdprConstants.VERSION_BIT_OFFSET, GdprConstants.VERSION_BIT_SIZE);
    
    #-- get when consent record created of Vendor
    #--- Record is present between  6 and 32 bits of consent string  
    
    def getConsentRecordCreated(self):
        return self.Bits.getInstantFromEpochDeciseconds(GdprConstants.CREATED_BIT_OFFSET, GdprConstants.CREATED_BIT_SIZE);

    #-- get when consent record updated of Vendor
    #--- Record is present between  42 and 36 bits of consent string  
    def getConsentRecordLastUpdated(self):
        return self.Bits.getInstantFromEpochDeciseconds(GdprConstants.UPDATED_BIT_OFFSET, GdprConstants.UPDATED_BIT_SIZE);
    
    #--  get CmpId of Vendor
    #--- Record is present between  78 and 12 bits of consent string  
    def getCmpId(self):
        return self.Bits.getInt(GdprConstants.CMP_ID_OFFSET, GdprConstants.CMP_ID_SIZE);

    #--  get Consent Screen of Vendor
    #--- Record is present between  102 and 6 bits of consent string  
    def getConsentScreen(self):
        return self.Bits.getInt(GdprConstants.CONSENT_SCREEN_OFFSET, GdprConstants.CONSENT_SCREEN_SIZE);
    
    #----get vendor list version of Vendor
    #--- Record is present between  102 and 6 bits of consent string  
    def getVendorListVersion(self):
        return self.Bits.getInt(GdprConstants.VENDOR_LIST_VERSION_OFFSET, GdprConstants.VENDOR_LIST_VERSION_SIZE);
    
    #----get allowed purpose bits version of Vendor
    #--- Record is present between  132 and 24 bits of consent string
    def getAllowedPurposesBits(self):
        return  self.Bits.getInt(GdprConstants.PURPOSES_OFFSET, GdprConstants.PURPOSES_SIZE);
    
    #----get max vendor id of Vendor
    #--- Record is present between  132 and 24 bits of consent string
    def getMaxVendorId(self):
        return  self.Bits.getInt(GdprConstants.MAX_VENDOR_ID_OFFSET, GdprConstants.MAX_VENDOR_ID_SIZE);
    
    #----get cmp version  of Vendor
    #--- Record is present between  90 and 12 bits of consent string
    def getCmpVersion(self):
        return self.Bits.getInt(GdprConstants.CMP_VERSION_OFFSET, GdprConstants.CMP_VERSION_SIZE);
    
    #----get consent language  of Vendor
    #--- Record is present between  108 and 12 bits of consent string
    def getConsentLanguage(self):
        return self.Bits.getSixBitString(GdprConstants.CONSENT_LANGUAGE_OFFSET, GdprConstants.CONSENT_LANGUAGE_SIZE);
    
    #----get allowed purpose ids
    #--- Record is present between  132 and 156 bits of consent string    
    def  getAllowedPurposeIds(self):
        allowedPurposes = set([]);
        for i in range(GdprConstants.PURPOSES_OFFSET, GdprConstants.PURPOSES_OFFSET+ GdprConstants.PURPOSES_SIZE):
            if (self.Bits.getBit(i)):
                allowedPurposes.add(i - GdprConstants.PURPOSES_OFFSET + 1);
        return list(allowedPurposes);
    
    #----is Purpose Allowed for the vendor
    def isPurposeAllowed(self, purposeId):
        if (purposeId < 1 or purposeId > GdprConstants.PURPOSES_SIZE):
            return False;
        return self.Bits.getBit(GdprConstants.PURPOSES_OFFSET + purposeId - 1);
    
    #---get encoding type of the vendor
    #--- Record is present between  172 and 1 bits of consent string  
    def encodingType(self):
        return self.Bits.getInt(GdprConstants.ENCODING_TYPE_OFFSET, GdprConstants.ENCODING_TYPE_SIZE);
    
    #---get allowed vendor ids 
    #--- allowed vendor ids are from 0 to maxVendorIds 
    def getAllowedVendorId(self):
        vendorIds = [];
        maxVendorIds = self.getMaxVendorId();
        vendorIds.extend(range(0, maxVendorIds+1))
        return vendorIds;
        
    
    def isVendorAllowed(self, vendorId):
        
        maxVendorId = self.getMaxVendorId();
        if (vendorId < 1 or vendorId > maxVendorId):
            return False;

        if (self.encodingType() == GdprConstants.VENDOR_ENCODING_RANGE):
            defaultConsent = self.Bits.getBit(GdprConstants.DEFAULT_CONSENT_OFFSET);
            present = self.isVendorPresentInRange(vendorId);
            return present != defaultConsent;
        else:
            return self.Bits.getBit(GdprConstants.VENDOR_BITFIELD_OFFSET + vendorId - 1);
    
    def isVendorPresentInRange(self, vendorId):
        
        numEntries = self.Bits.getInt(GdprConstants.NUM_ENTRIES_OFFSET, GdprConstants.NUM_ENTRIES_SIZE);
        maxVendorId = self.getMaxVendorId();
        
        currentOffset = GdprConstants.RANGE_ENTRY_OFFSET;
        
        for i in range(numEntries):
            currentOffset = currentOffset + 1;
            if self.Bits.getBit(currentOffset) > 0: 
                startVendorId = self.Bits.getInt(currentOffset, GdprConstants.VENDOR_ID_SIZE);
                currentOffset += GdprConstants.VENDOR_ID_SIZE;
                endVendorId = self.Bits.getInt(currentOffset, GdprConstants.VENDOR_ID_SIZE);
                currentOffset += GdprConstants.VENDOR_ID_SIZE;

                if (startVendorId > endVendorId or endVendorId > maxVendorId):
                    raise ValueError(
                            "Start VendorId must not be greater than End VendorId and "
                                    +"End VendorId must not be greater than Max Vendor Id");
                                    
                if (vendorId >= startVendorId and vendorId <= endVendorId): return True;

            else:
                singleVendorId = self.Bits.getInt(currentOffset, GdprConstants.VENDOR_ID_SIZE);
                currentOffset += GdprConstants.VENDOR_ID_SIZE;

                if (singleVendorId > maxVendorId) :
                    raise ValueError(
                            "VendorId in the range entries must not be greater than Max VendorId");

                if (singleVendorId == vendorId): return True;
        return False;

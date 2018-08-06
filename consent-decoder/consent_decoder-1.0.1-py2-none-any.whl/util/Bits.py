import datetime
import time


class Bits:
    
    bytes;
    bytePows = [-128, 64, 32, 16, 8, 4, 2, 1 ];
    
    dateFormat = "%Y-%m-%dT%H:%M:%S.%fZ"
    
    #--- Contructor----
    def __init__(self, bytes):
        self.bytes = bytes;
    
    #--- get bit 1/0  on given index
    def getBit(self, index):
        byteIndex = index / 8
        bitExact = index % 8;
        byte = self.bytes[int(byteIndex)];
        return (byte & self.bytePows[bitExact]) != 0;
    
    #--- set bit 1/0  on given index
    def setBit(self, index):
        byteIndex = index / 8;
        shift = (byteIndex + 1) * 8 - index - 1;
        self.bytes[byteIndex] |= 1 << shift;
   
    #--- set bit 0 on given index
    def unsetBit(self, index):
        byteIndex = index / 8;
        shift = (byteIndex + 1) * 8 - index - 1;
        self.bytes[byteIndex] &= ~(1 << shift);
        
    #------ get sixth bit character  from start to end
    def getSixBitString(self, startInclusive, size):
        if (size % 6 != 0):
            raise("string bit length must be multiple of six: " + str(size));
        
        charNum = size / 6;
        val = '';
        for i in range(int(charNum)):
            charCode = self.getInt(startInclusive + (i * 6), 6) + 65;
            val = val + chr(charCode);
        
        return val.upper();
    
    #-------get long velue within given bit range
    def getLong(self, startInclusive, size):
        
        val = 0;
        sigMask = 1;
        sigIndex = size - 1;
        
        for i in range(0, size):
            if (self.getBit(startInclusive + i)):
                val += (sigMask << sigIndex);
            sigIndex = sigIndex - 1;
            
        return val;
    
    #-------get date within given bit range
    def getInstantFromEpochDeciseconds(self, startInclusive, size):
        epochDemi = self.getLong(startInclusive, size);
        return self.datetime_to_utc(datetime.datetime.fromtimestamp(epochDemi / 10.0).strftime(self.dateFormat))
    
    def datetime_to_utc(self, date):
        timestamp = str(time.mktime(datetime.datetime.strptime(date, self.dateFormat).timetuple()))[:-2]
        return datetime.datetime.utcfromtimestamp(int(timestamp)).strftime(self.dateFormat)
    
    #-------get long velue within given bit range
    def getInt(self, startInclusive, size):
        val = 0;
        sigMask = 1;
        sigIndex = size - 1;

        for i in range(0, size):
            if (self.getBit(startInclusive + i)):
                val += (sigMask << sigIndex)
             
            sigIndex = sigIndex - 1; 
        return val;
    
    def toByteArray(self):
        return self.bytes;
    

#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2014  Jonathan Delvaux <apdu@djoproject.net>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#TODO
    #Recollection Card – 1, 2, 4, 8 and 18 Kbit I2C Card          XXX OK 
    #Memory Card – 32, 64, 128, 256, 512, and 1024 Kbit I2C Card  XXX OK 
    #Memory Card – ATMEL AT88SC153                                TODO verify pin is so strange...
    #Memory Card – ATMEL AT88C1608                                TODO
    #Memory Card – SLE 4418 / SLE 4428 / SLE 5518 / SLE 5528      TODO 
    #Memory Card – SLE 4432 / SLE 4442 / SLE 5532 / SLE 5542      TODO 
    #Memory Card – SLE 4406 / SLE 4436 / SLE 5536 / SLE 6636      TODO 
    #Memory Card – SLE 4404                                       TODO
    #Memory Card – AT88SC101 / AT88S C102 / AT88S C1003           TODO 
    #Other Commands Access via PC_to_RDR_XfrBlock                 TODO



from apdu.standard.iso7816_4 import iso7816_4APDUBuilder
from apdu.misc.apdu import ApduDefault
from apdu.misc.exception import apduBuilderException

class acr38uAPDUBuilder(iso7816_4APDUBuilder):
    
    ACR38SW = {0x90:{0xFF:"SLOTERROR_CMD_ABORTED",
                     0xFE:"SLOTERROR_ICC_MUTE",
                     0xFD:"SLOTERROR_XFR_PARITY_ERROR",
                     0xFC:"SLOTERROR_XFR_OVERRUN",
                     0xFB:"SLOTERROR_HW_ERROR",
                     0xF8:"SLOTERROR_BAD_ATR_TS",
                     0xF7:"SLOTERROR_BAD_ATR_TCK",
                     0xF6:"SLOTERROR_ICC_PROTOCOL_NOT_SUPPORTED",
                     0xF5:"SLOTERROR_PROCEDURE_BYTE_CONFLICE",
                     0xF4:"SLOTERROR_PROCEDURE_BYTE_CONFLICE",
                     0xF3:"SLOTERROR_DEACTIVATED_PROTOCOL",
                     0xF2:"SLOTERROR_BUSY_WITH_AUTO_SEQUENCE",
                     0xF0:"SLOTERROR_CMD_SLOT_BUSY"}}
    
### default command ###
    
    @staticmethod
    def getReaderInformation():
        return ApduDefault(cla=0xFF,ins=0x09,p1=0x00,p2=0x00,expected_answer=0x10)
    
    TYPE_AUTO               = 0x00
    TYPE_I2C_1KTO16K        = 0x01
    TYPE_I2C_32KTO1024K     = 0x02
    TYPE_AT88SC153          = 0x3
    TYPE_AT88SC1608         = 0x4
    TYPE_SLEXX18_XX28       = 0x5
    TYPE_SLEXX32_XX42       = 0x6
    TYPE_SLEXX06_XX36       = 0x7
    TYPE_SLE4404            = 0x8
    TYPE_AT88SC101_102_1003 = 0x9
    TYPE_RFU1               = 0xA
    TYPE_RFU2               = 0xB
    TYPE_MCU_T0             = 0xC
    TYPE_MCU_T1             = 0xD

    SELECT_TYPE = {"AUTO"               : TYPE_AUTO,
                   "I2C_1KTO16K"        : TYPE_I2C_1KTO16K,
                   "I2C_32KTO1024K"     : TYPE_I2C_32KTO1024K,
                   "AT88SC153"          : TYPE_AT88SC153,
                   "AT88SC1608"         : TYPE_AT88SC1608,
                   "SLE2"               : TYPE_SLEXX32_XX42,
                   "SLE4"               : TYPE_SLE4404,
                   "SLE6"               : TYPE_SLEXX06_XX36,
                   "SLE8"               : TYPE_SLEXX18_XX28,
                   "AT88SC101_102_1003" : TYPE_AT88SC101_102_1003,
                   "RFU1"               : TYPE_RFU1,
                   "RFU2"               : TYPE_RFU2,
                   "MCU_T0"             : TYPE_MCU_T0,
                   "MCU_T1"             : TYPE_MCU_T1}
        
    @staticmethod
    def selectType(TYPE = TYPE_AUTO):
        if TYPE < 0 or TYPE > 0xD:
            raise apduBuilderException("invalid argument TYPE, a value between 0 and 13 was expected, got "+str(TYPE))
        
        apdu = ApduDefault(cla=0xFF,ins=0xA4,p1=0x00,p2=0x00,data=[TYPE])
        apdu.removeExpectedAnswer()
        return apdu
    
    READ_AREA_0    = 0xb0
    READ_AREA_1    = 0xb1
    READ_AREA_2    = 0xb2
    READ_AREA_3    = 0xb3
    READ_AREA_FUSE = 0xb4
    
    WRITE_AREA_0    = 0xd0
    WRITE_AREA_1    = 0xd1
    WRITE_AREA_2    = 0xd2
    WRITE_AREA_3    = 0xd3
    WRITE_AREA_FUSE = 0xd4
    
    @staticmethod
    def read(adress, length=0, area = READ_AREA_0):
        if adress < 0 or adress > 0x1ffff:
            raise apduBuilderException("invalid argument adress, a value between 0 and 1023 was expected, got "+str(TYPE))

        if length < 0 or length > 0xff:
            raise apduBuilderException("invalid argument length, a value between 0 and 255 was expected, got "+str(length))

        if area < 0xb0 or area > 0xb4:
            raise apduBuilderException("invalid argument area, a value between 0xb0 and 0xb4 was expected, got "+str(area))

        if adress >= 0x10000:
            area |= 0x1

        msb = (adress >> 8) & 0xFF
        lsb = adress & 0xFF

        return ApduDefault(cla=0xFF,ins=area,p1=msb,p2=lsb, expected_answer=length)

    @staticmethod
    def write(adress, datas, area = WRITE_AREA_0):
        if adress < 0 or adress > 0x1ffff:
            raise apduBuilderException("invalid argument adress, a value between 0 and 1023 was expected, got "+str(TYPE))

        if len(datas) < 1 or len(datas) > 255:
            raise apduBuilderException("invalid datas size, must be a list from 1 to 255 item, got "+str(len(datas)))

        if area < 0xd0 or area > 0xd4:
            raise apduBuilderException("invalid argument area, a value between 0xd0 and 0xd4 was expected, got "+str(area))

        if adress >= 0x10000:
            area |= 0x1

        msb = (adress >> 8) & 0xFF
        lsb = adress & 0xFF

        apdu = ApduDefault(cla=0xFF,ins=area,p1=msb,p2=lsb, data=datas)
        apdu.removeExpectedAnswer()
        return apdu
        
### I2C card ###

    I2C_PAGE_SIZE_8BYTES    = 0x03
    I2C_PAGE_SIZE_16BYTES   = 0x04
    I2C_PAGE_SIZE_32BYTES   = 0x05
    I2C_PAGE_SIZE_64BYTES   = 0x06
    I2C_PAGE_SIZE_128BYTES  = 0x07
    I2C_PAGE_SIZE_256BYTES  = 0x08 #XXX not in documentation, maybe wrong value...
    I2C_PAGE_SIZE_512BYTES  = 0x09 #XXX not in documentation, maybe wrong value...
    I2C_PAGE_SIZE_1024BYTES = 0x0A #XXX not in documentation, maybe wrong value...
    

    I2C_PAGE_SIZE = {
                     "8BYTES"    : I2C_PAGE_SIZE_8BYTES,
                     "16BYTES"   : I2C_PAGE_SIZE_16BYTES,
                     "32BYTES"   : I2C_PAGE_SIZE_32BYTES,
                     "64BYTES"   : I2C_PAGE_SIZE_64BYTES,
                     "128BYTES"  : I2C_PAGE_SIZE_128BYTES,
                     "256BYTES"  : I2C_PAGE_SIZE_256BYTES,
                     "512BYTES"  : I2C_PAGE_SIZE_512BYTES,
                     "1024BYTES" : I2C_PAGE_SIZE_1024BYTES,
    }

    @staticmethod
    def I2C_selectPageSize(page_size = I2C_PAGE_SIZE_8BYTES):
        if page_size < 0x03 or page_size > 0x0A:
            raise apduBuilderException("invalid argument page_size, a value between 0x03 and 0x07 was expected, got "+str(page_size))
    
        apdu = ApduDefault(cla=0xFF,ins=0x01,p1=0x00,p2=0x00, data=(page_size,))
        apdu.removeExpectedAnswer()
        return apdu
        
### ATMEL command ###
    


### SLE command ###

    @staticmethod
    def SLE_checkPinCode(pinBytes):
        if len(pinBytes) < 2 or len(pinBytes) > 3:
            raise apduBuilderException("invalid argument pinBytes, a list of bytes of lenght 2 or 3 was expected, got "+str(len(pinBytes)))
    
        apdu = ApduDefault(cla=0xFF,ins=0x20,p1=0x00,p2=0x00, data=pinBytes)
        apdu.removeExpectedAnswer()
        return apdu
        
    @staticmethod
    def SLE_changePinCode(pinBytes):
        pass #TODO
        
    def SLE_getErrorCounter(expected = 3):
        
    
        return acr38uAPDUBuilder.read(0,3,READ_AREA_1)

    def SLE_readProtectionBit(address, numberOfBit):
        if numberOfBit < 0:
            raise apduBuilderException("invalid argument numberOfBit, a value bigger or equal than 0 was expected, got "+str(numberOfBit))
        
        return acr38uAPDUBuilder.read(address, 1 + int( (n-1)/8. ) ,READ_AREA_1)

    def SLE_writeProtectionBit(address, bits_list):
        bits = 0 #TODO
        
        return acr38uAPDUBuilder.write(address, bits,READ_AREA_1)
        

        



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
	#it looks like a draft

from apdu.standard.iso7816_4 import iso7816_4APDUBuilder
from apdu.misc.apdu import ApduDefault
from apdu.misc.exception import apduBuilderException

class acr38uAPDUBuilder(iso7816_4APDUBuilder):
    
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
                   "SLEXX18_XX28"       : TYPE_SLEXX18_XX28,
                   "SLEXX32_XX42"       : TYPE_SLEXX32_XX42,
                   "SLEXX06_XX36"       : TYPE_SLEXX06_XX36,
                   "SLE4404"            : TYPE_SLE4404,
                   "AT88SC101_102_1003" : TYPE_AT88SC101_102_1003,
                   "RFU1"               : TYPE_RFU1,
                   "RFU2"               : TYPE_RFU2,
                   "MCU_T0"             : TYPE_MCU_T0,
                   "MCU_T1"             : TYPE_MCU_T1}
    
    @staticmethod
    def getReaderInformation():
        return ApduDefault(cla=0xFF,ins=0x09,p1=0x00,p2=0x00,expected_answer=0x10)
    
    @staticmethod
    def selectType(TYPE = 0):
        if TYPE < 0 or TYPE > 0xD:
            raise apduBuilderException("invalid argument TYPE, a value between 0 and 13 was expected, got "+str(TYPE))
        
        apdu = ApduDefault(cla=0xFF,ins=0xA4,p1=0x00,p2=0x00,data=[TYPE])
        apdu.removeExpectedAnswer()
        return apdu

    @staticmethod
    def read(adress, length=0):
        if adress < 0 or adress > 0x3ff:
            raise apduBuilderException("invalid argument adress, a value between 0 and 1023 was expected, got "+str(TYPE))

        if length < 0 or length > 0xff:
            raise apduBuilderException("invalid argument length, a value between 0 and 255 was expected, got "+str(length))

        msb = (adress >> 8) & 0xFF
        lsb = adress & 0xFF

        return ApduDefault(cla=0xFF,ins=0xb0,p1=msb,p2=lsb, expected_answer=length)

    @staticmethod
    def write(adress, datas):
        if adress < 0 or adress > 0x3ff:
            raise apduBuilderException("invalid argument adress, a value between 0 and 1023 was expected, got "+str(TYPE))

        if len(datas) < 1 or len(datas) > 255:
            raise apduBuilderException("invalid datas size, must be a list from 1 to 255 item, got "+str(len(datas)))

        msb = (adress >> 8) & 0xFF
        lsb = adress & 0xFF

        apdu = ApduDefault(cla=0xFF,ins=0xD0,p1=msb,p2=lsb, data=datas)
        apdu.removeExpectedAnswer()
        return apdu

    @staticmethod
    def checkPinCode(pinBytes):
        apdu = ApduDefault(cla=0xFF,ins=0x20,p1=0x00,p2=0x00, data=pinBytes)
        apdu.removeExpectedAnswer()
        return apdu

    #TODO
        #change pin
        #set/get security bit
            #DO NOT TEST !!!!
        #get retry counter
        #test everything on sle 5542



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

from apdu.readers.acr122v1   import acr122SamAPDUBuilder
from apdu.standard.iso7816_4 import iso7816_4APDUBuilder
from apdu.misc.apdu          import ApduDefault, ApduRaw
from apdu.misc.exception     import apduBuilderException

class acr122APDUBuilder(acr122SamAPDUBuilder):
    @staticmethod
    def getDataCardSerialNumber():
        "acr122 card serial"
        return iso7816_4APDUBuilder.getDataCA(0x00,0x00)
    
    @staticmethod
    def getDataCardATS():
        "acr122 card historic byte"
        return iso7816_4APDUBuilder.getDataCA(0x01,0x00)
        
    @staticmethod
    def loadKey(KeyName,KeyIndex=0):
        if KeyName not in keys:
            raise apduBuilderException("the key name doesn't exist "+str(KeyName))
            
        if len(keys[KeyName]) != 6:
            raise apduBuilderException("invalid key length, must be 6, got "+str(len(keys[KeyName])))
        
        if KeyIndex < 0x0 or KeyIndex > 0x1:
            raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 1 was expected, got "+str(KeyIndex))
    
        #P1 === load into volatile memory
        return ApduDefault(cla=0xFF,ins=0x82,p1=0x00,p2=KeyIndex,data=keys[KeyName])

    @staticmethod
    def authentificationObsolete(blockNumber,KeyIndex=0,isTypeA = True):
        
        if blockNumber < 0x0 or blockNumber > 0xFF:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        if KeyIndex < 0x0 or KeyIndex > 0x1:
            raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 1 was expected, got "+str(KeyIndex))
        
        if isTypeA:
            return ApduRaw([0xFF,0x88,0x00,blockNumber,0x60,KeyIndex])
        else:
            return ApduRaw([0xFF,0x88,0x00,blockNumber,0x61,KeyIndex])
        
    @staticmethod
    def authentification(blockNumber=0,KeyIndex=0,isTypeA = True):
        if blockNumber < 0x0 or blockNumber > 0xFF:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        if KeyIndex < 0x0 or KeyIndex > 0x1:
            raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 1 was expected, got "+str(KeyIndex))
        
        if isTypeA:
            return ApduDefault(cla=0xFF,ins=0x86,p1=0x00,p2=0x00,data=[0x01,0x00,blockNumber,0x60,KeyIndex])
        else:
            return ApduDefault(cla=0xFF,ins=0x86,p1=0x00,p2=0x00,data=[0x01,0x00,blockNumber,0x61,KeyIndex])
        
    @staticmethod
    def readBinary(blockNumber=0,byteToRead=0):
        if byteToRead < 0x0 or byteToRead > 0xFF:
            raise apduBuilderException("invalid argument byteToRead, a value between 0 and 255 was expected, got "+str(byteToRead))
        
        if blockNumber < 0x0 or blockNumber > 0xFF:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        return ApduDefault(cla=0xFF,ins=0xB0,p1=0x00,p2=blockNumber,data=[],expected_answer=byteToRead)
        
    @staticmethod
    def updateBinary(bytes,blockNumber=0):
        if len(bytes) < 1 or len(bytes) > 255:
            raise apduBuilderException("invalid args bytes, must be a list from 1 to 255 item, got "+str(len(bytes)))
        
        if blockNumber < 0x0 or blockNumber > 0xFF:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        return ApduDefault(cla=0xFF,ins=0xD6,p1=0x00,p2=blockNumber,data=bytes)
    
    #0x00 = set, 0x01 = inc, 0x02 = dec
    #value is signed
    @staticmethod
    def valueBlockOperationDec(operation,value=0,blockNumber=0):
        if blockNumber < 0x0 or blockNumber > 0xFF:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        if operation < 0x0 or operation > 0x03:
            raise apduBuilderException("invalid argument operation, a value between 0 and 255 was expected, got "+str(operation))

        if value < -0x10000000 or value > 0xEFFFFFFF:
            raise apduBuilderException("invalid argument value, a value between -2147483648 and 2147483647 was expected, got "+str(value))

        if value < 0:
            value = 0xFFFFFFFF + (value + 1)

        B4 = value&0xFF
        B3 = (value>>8)&0xFF
        B2 = (value>>16)&0xFF
        B1 = (value>>24)&0xFF

        return ApduDefault(cla=0xFF,ins=0xD7,p1=0x00,p2=blockNumber,data=[B1,B2,B3,B4])
    
    @staticmethod
    def valueBlockOperationSet(value=0,blockNumber=0):
        return valueBlockOperationDec(0x00,value,blockNumber)
        
    @staticmethod
    def valueBlockOperationInc(value=0,blockNumber=0):
        return valueBlockOperationDec(0x01,value,blockNumber)
            
    @staticmethod
    def valueBlockOperationDec(value=0,blockNumber=0):
        return valueBlockOperationDec(0x02,value,blockNumber)
        
    @staticmethod
    def readValueBlock(blockNumber=0):
        if blockNumber < 0x0 or blockNumber > 0xFF:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
            
        return ApduDefault(cla=0xFF,ins=0xB1,p1=0x00,p2=blockNumber,data=[],expected_answer=0x04)
        
    @staticmethod
    def restoreValueBlock(source,target):
        if source < 0x0 or source > 0xFF:
            raise apduBuilderException("invalid argument source, a value between 0 and 255 was expected, got "+str(source))
        
        if target < 0x0 or target > 0xFF:
            raise apduBuilderException("invalid argument target, a value between 0 and 255 was expected, got "+str(target))
        
        return ApduDefault(cla=0xFF,ins=0xD7,p1=0x00,p2=source,data=[0x03,target])
        
    @staticmethod
    def getPICCOperatingParameter():
        "acr122 get picc parameter"
        return ApduDefault(cla=0xFF,ins=0x00,p1=0x50,p2=0x01)
        
    def setPICCOperatingParameter(param):
        if param < 0x0 or param > 0xFF:
            raise apduBuilderException("invalid argument param, a value between 0 and 255 was expected, got "+str(param))
            
        return ApduDefault(cla=0xFF,ins=0x00,p1=0x51,p2=param)
        
    @staticmethod
    def setTimeoutParameter(value):
        if value < 0x0 or value > 0xFF:
            raise apduBuilderException("invalid argument value, a value between 0 and 255 was expected, got "+str(value))
        
        return ApduDefault(cla=0xFF,ins=0x00,p1=0x41,p2=value)
        
    @staticmethod
    def setBuzzerOutputEnable(enable=True):
        if enable:
            return ApduDefault(cla=0xFF,ins=0x00,p1=0x52,p2=0xFF) 
        else:
            return ApduDefault(cla=0xFF,ins=0x00,p1=0x52,p2=0x00) 


def PICCOperatingParameter(autopolling,autoats,polling,felica424K,felica212K,topaz,iso14443B,iso14443A):
    return acr122APDUBuilder.setPICCOperatingParameter(autopolling|autoats|polling|felica424K|felica212K|topaz|iso14443B|iso14443A)


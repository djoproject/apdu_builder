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

from apdu.misc.apdu import ApduDefault
from apdu.standard.iso7816_4 import iso7816_4APDUBuilder
from apdu.misc.exception import apduBuilderException

class scl3711APDUBuilder(iso7816_4APDUBuilder):
    
    @staticmethod 
    def getDataCardSerialNumber():
        return iso7816_4APDUBuilder.getDataCA(0x00,0x00)
        
    @staticmethod
    def getDataCardATS():
        return iso7816_4APDUBuilder.getDataCA(0x01,0x00)
            
    @staticmethod
    def encapsulate(datas):
        #TODO limite de 255
        
        return ApduDefault(cla=0xFF,ins=0xFE,p1=0x00,p2=0x00,data=datas)
        
    @staticmethod
    def sendDataPassThrough(datas):
        #TODO limite de 255
        
        return ApduDefault(cla=0xFF,ins=0xFE,p1=0x00,p2=0x00,data=datas)
        
    @staticmethod
    def readBinary(address = 0):
        if address < 0 or address > 255:
            raise apduBuilderException("invalid argument address, a value between 0 and 255 was expected, got "+str(address))

        return ApduDefault(cla=0xFF,ins=0xB0,p1=0x00,p2=address&0xFF)
        
    @staticmethod
    def updateBinary(datas,address=0):
        if address < 0 or address > 255:
            raise apduBuilderException("invalid argument address, a value between 0 and 255 was expected, got "+str(address))

        if len(datas) < 1 or len(datas) > 255:
            raise apduBuilderException("invalid datas size, must be a list from 1 to 255 item, got "+str(len(datas)))

        return ApduDefault(cla=0xFF,ins=0xD6,p1=0x00,p2=address&0xFF,data=datas)
    
    @staticmethod
    def loadKey(KeyName,isTypeA = True):
        #TODO KeyName
        
        if len(Key) != 6:
            raise apduBuilderException("invalid key size, must be 6, got "+str(len(Key)))

        if isTypeA:
            P2 = 0x60
        else:
            P2 = 0x61
            
        return ApduDefault(cla=0xFF,ins=0x82,p1=0x00,p2=P2,data=Key)
        
    @staticmethod
    def generalAuthenticate(blockNumber,isTypeA = True,KeyIndex = 0):
        if blockNumber < 0 or blockNumber > 65535:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 65535 was expected, got "+str(blockNumber))

        lsb = address&0xFF
        msb = (address>>8)&0xFF

        if KeyIndex < 0 or KeyIndex > 255: #verification hasardeuse, le nombre de cle dans la doc n'est pas dis
            raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 255 was expected, got "+str(KeyIndex))

        if isTypeA:
            datas = [0x01,msb,lsb,0x60,KeyIndex]
        else:
            datas = [0x01,msb,lsb,0x61,KeyIndex]

        return ApduDefault(cla=0xFF,ins=0x88,p1=0x00,p2=0x00,data=datas)
            
    @staticmethod
    def increment(address=0,value=0x01,increment=True):
        if address < 0 or address > 255:
            raise apduBuilderException("invalid argument address, a value between 0 and 255 was expected, got "+str(address))

        if value < 0 or value > 0xFFFFFFFF:
            raise apduBuilderException("invalid argument value, a value between 0 and 4294967295 was expected, got "+str(value))
            
        if increment:
            return ApduDefault(cla=0xFF,ins=0xF0,p1=0x00,p2=address,data=[0xC0,address,value&0xFF,(value>>8)&0xFF,(value>>16)&0xFF,(value>>24)&0xFF])
        else:
            return ApduDefault(cla=0xFF,ins=0xF0,p1=0x00,p2=address,data=[0xC1,address,value&0xFF,(value>>8)&0xFF,(value>>16)&0xFF,(value>>24)&0xFF])
            
            
    @staticmethod
    def userToken():
        pass #TODO doc officiel incomplete...
        
    #@staticmethod
    #def desfireApdu(apdu):
    #    return apdu
    
    @staticmethod
    def nfcType1ReadIdentification():
        return ApduDefault(cla=0xFF,ins=0x50)

    @staticmethod
    def nfcType1ReadAll():
        return ApduDefault(cla=0xFF,ins=0x52)
        
    @staticmethod
    def nfcType1ReadByte(byteNumber=0,blockNumber=0):
        if byteNumber < 0 or byteNumber > 7:
            raise apduBuilderException("invalid argument byteNumber, a value between 0 and 7 was expected, got "+str(byteNumber))
        
        if blockNumber < 0 or blockNumber > 0xE:
            raise apduBuilderException("invalid argument byteNumber, a value between 0 and 14 was expected, got "+str(byteNumber))
        
        P2 = (byteNumber&0x7) | ((blockNumber&0x0f)<<3)
        
        return ApduDefault(cla=0xFF,ins=0x54,p1=0x00,p2=P2)
    
    @staticmethod
    def nfcType1WriteByte(byteValue,byteNumber=0,blockNumber=0,erase=True):
        if byteValue < 0 or byteValue > 255:
            raise apduBuilderException("invalid argument byteValue, a value between 0 and 255 was expected, got "+str(byteValue))
        
        if byteNumber < 0 or byteNumber > 7:
            raise apduBuilderException("invalid argument byteNumber, a value between 0 and 7 was expected, got "+str(byteNumber))
        
        if blockNumber < 0 or blockNumber > 0xE:
            raise apduBuilderException("invalid argument byteNumber, a value between 0 and 14 was expected, got "+str(byteNumber))
        
        P2 = (byteNumber&0x7) | ((blockNumber&0x0f)<<3)
        
        if erase:
            return ApduDefault(cla=0xFF,ins=0x56,p1=0x00,p2=P2,data=[byteValue])
        else:
            return ApduDefault(cla=0xFF,ins=0x58,p1=0x00,p2=P2,data=[byteValue])
    
    @staticmethod
    def nfcType1ReadSegment(address=0):
        if address < 0 or address > 0xF:
            raise apduBuilderException("invalid argument address, a value between 0 and 15 was expected, got "+str(address))
    
        return ApduDefault(cla=0xFF,ins=0x5A,p1=0x00,p2=((address&0xF)<<4))
    
    @staticmethod
    def nfcType1Read8bytes(address=0):
        if address < 0 or address > 0xFF:
            raise apduBuilderException("invalid argument address, a value between 0 and 255 was expected, got "+str(address))

        return ApduDefault(cla=0xFF,ins=0x5C,p1=0x00,p2=address)
    
    @staticmethod
    def nfcType1Write8Bytes(bytes,address=0,erase=True):
        if address < 0 or address > 0xFF:
            raise apduBuilderException("invalid argument address, a value between 0 and 255 was expected, got "+str(address))
            
        if len(bytes) != 8:
            raise apduBuilderException("invalid bytes size, must be a list of 8 item, got "+str(len(bytes)))
        
        if erase:
            return ApduDefault(cla=0xFF,ins=0x5E,p1=0x00,p2=address,data=bytes)
        else:
            return ApduDefault(cla=0xFF,ins=0x60,p1=0x00,p2=address,data=bytes)
        
    @staticmethod
    def nfcType3REQC(serviceCode,RFU,TSN):
        if serviceCode < 0 or serviceCode > 0xFFFF:
            raise apduBuilderException("invalid argument serviceCode, a value between 0 and 65535 was expected, got "+str(serviceCode))
        
        if RFU < 0 or RFU > 0xFF:
            raise apduBuilderException("invalid argument RFU, a value between 0 and 255 was expected, got "+str(RFU))
        
        if TSN < 0 or TSN > 0xFF:
            raise apduBuilderException("invalid argument TSN, a value between 0 and 255 was expected, got "+str(TSN))
            
        return ApduDefault(cla=0xFF,ins=0x40,p1=0x00,p2=0x00,data=[(serviceCode>>8)&0xFF,serviceCode&0xFF,RFU,TSN])
        
    @staticmethod
    def nfcType3RequestService(ServiceCodeList):
        
        Data = []
        for s in ServiceCodeList:
            if s < 0 or s > 0xFFFF:
                raise apduBuilderException("invalid argument in service code list, a value between 0 and 65535 was expected, got "+str(s))
                
            lsb = s&0xFF
            msb = (s>>8)&0xFF
            
            Data.extend([msb,lsb])
        
        return ApduDefault(cla=0xFF,ins=0x42,p1=len(ServiceCodes),p2=0x00,data=Data)
        
    @staticmethod
    def nfcType3RequestRespons():
        return ApduDefault(cla=0xFF,ins=0x44)
        
    @staticmethod
    def nfcType3Read(ServiceCodeList,BlockCodeList):
        Data = []
        for s in ServiceCodeList:
            if s < 0 or s > 0xFFFF:
                raise apduBuilderException("invalid argument in service code list, a value between 0 and 65535 was expected, got "+str(s))
                
            lsb = s&0xFF
            msb = (s>>8)&0xFF
            
            Data.extend([msb,lsb])
            
        for s in BlockCodeList:
            if s < 0 or s > 0xFFFF:
                raise apduBuilderException("invalid argument in block code list, a value between 0 and 65535 was expected, got "+str(s))

            lsb = s&0xFF
            msb = (s>>8)&0xFF

            Data.extend([msb,lsb])
        
        return ApduDefault(cla=0xFF,ins=0x46,p1=len(ServiceCodes),p2=len(BlockCodes),data=Data)
        
    @staticmethod
    def nfcType3Write(ServiceCodeList,BlockCodeList,DataList):
        #check len(BlockCodeList) vs len(DataList)
        if len(BlockCodeList) * 16 != len(DataList):
            raise apduBuilderException("invalid DataList size, must be a list equals to "+str(len(BlockCodeList) * 16)+" bytes, got "+str(len(DataList)))
        
        Data = []
        for s in ServiceCodeList:
            if s < 0 or s > 0xFFFF:
                raise apduBuilderException("invalid argument in service code list, a value between 0 and 65535 was expected, got "+str(s))
                
            lsb = s&0xFF
            msb = (s>>8)&0xFF
            
            Data.extend([msb,lsb])
            
        for s in BlockCodeList:
            if s < 0 or s > 0xFFFF:
                raise apduBuilderException("invalid argument in block code list, a value between 0 and 65535 was expected, got "+str(s))

            lsb = s&0xFF
            msb = (s>>8)&0xFF

            Data.extend([msb,lsb])
            
        #append DataList
        Data.extend(DataList)
        
        return ApduDefault(cla=0xFF,ins=0x48,p1=len(ServiceCodes),p2=len(BlockCodes),data=Data)
        
    @staticmethod
    def nfcType3RequestSystemCode():
        return ApduDefault(cla=0xFF,ins=0x4A)
        


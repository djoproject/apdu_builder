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

from apdu.misc.apdu import Apdu
from apdu.misc.exception import apduBuilderException

class ApduPn53x(Apdu):
    def __init__(self,ins,data = []):
        self.extend([0xD4,ins])
        if len(data) > 0:
            self.extend(data)

class pn532APDUBuilder(object):
    
    #Miscellaneous
    
    @staticmethod
    def Diagnose():
        pass#TODO
    
    @staticmethod
    def GetFirmwareVersion():
        "get firmware version"
        
        return ApduPn53x(0x02)
    
    @staticmethod
    def GetGeneralStatus():
        return ApduPn53x(0x04)
    
    @staticmethod
    def ReadRegister():
        pass#TODO
    
    @staticmethod
    def WriteRegister():
        pass#TODO
    
    @staticmethod
    def ReadGPIO():
        return ApduPn53x(0x0c)
    
    @staticmethod
    def WriteGPIO():
        pass#TODO
    
    @staticmethod
    def SetSerialBaudRate():
        pass#TODO
    
    @staticmethod
    def SetParameters():
        pass#TODO
    
    @staticmethod
    def SAMConfiguration():
        pass#TODO
    
    @staticmethod
    def PowerDown():
        pass#TODO
    
    #RF communication
    
    @staticmethod
    def RFConfiguration():
        pass#TODO
    
    @staticmethod
    def RFRegulationTest():
        pass#TODO
    
    #Initiator
    
    @staticmethod
    def InJumpForDEP():
        pass#TODO
    
    @staticmethod
    def InJumpForPSL():
        pass#TODO
    
    #poll
    BrTyTypeA = 0x00
    BrTyFelica212 = 0x01
    BrTyFelica424 = 0x02
    BrTyTypeB = 0x03
    BrTyInnovisionJewel = 0x04
    
    @staticmethod
    def InListPassiveTarget(BrTy,MaxTg=1,InitiatorData=[]):
        if MaxTg < 1 or MaxTg > 2:
            raise apduBuilderException("invalid argument MaxTg, a value between 1 and 2 was expected, got "+str(MaxTg))
    
        if BrTy < 0 or BrTy > 4:
            raise apduBuilderException("invalid argument BrTy, a value between 0 and 4 was expected, got "+str(BrTy))
    
        data = [MaxTg,BrTy]
        data.extend(InitiatorData)
        return ApduPn53x(0x4A,data)
        
    @staticmethod
    def InATR():
        pass#TODO
    
    @staticmethod
    def InPSL():
        pass#TODO
    
    @staticmethod
    def InDataExchange(target,args=[]):
        if target < 1 or target > 2:
            raise apduBuilderException("invalid argument target, a value between 1 and 2 was expected, got "+str(target))
        
        return ApduPn53x(0x02,args)
    
    @staticmethod
    def InCommunicateThru():
        pass#TODO
    
    AllTarget = 0x00
    Target1 = 0x01
    Target2 = 0x02
    
    @staticmethod
    def InDeselect(target = 0):
        if target < 0 or target > 2:
            raise apduBuilderException("invalid argument target, a value between 0 and 2 was expected, got "+str(target))
            
        return ApduPn53x(0x44,[target])
    
    @staticmethod
    def InRelease(target = 0):
        if target < 0 or target > 2:
            raise apduBuilderException("invalid argument target, a value between 0 and 2 was expected, got "+str(target))
            
        return ApduPn53x(0x52,[target])
    
    @staticmethod
    def InSelect():
        if target < 0 or target > 2:
            raise apduBuilderException("invalid argument target, a value between 0 and 2 was expected, got "+str(target))
            
        return ApduPn53x(0x54,[target])
    
    @staticmethod
    def InAutoPoll():
        pass#TODO
    
    #Target
    
    @staticmethod
    def TgInitAsTarget():
        pass#TODO
    
    @staticmethod
    def TgSetGeneralBytes():
        pass#TODO
    
    @staticmethod
    def TgGetData():
        return ApduPn53x(0x86)
    
    @staticmethod
    def TgSetData():
        pass#TODO
    
    @staticmethod
    def TgSetMetaData():
        pass#TODO
    
    @staticmethod
    def TgGetInitiatorCommand():
        return ApduPn53x(0x88)
    
    @staticmethod
    def TgResponseToInitiator():
        pass#TODO
    
    @staticmethod
    def TgGetTargetStatus():
        return ApduPn53x(0x8A)

def pn532StatusToString(Status):
    if Status == 0x00:
        return "success"
    elif Status == 0x01:
        return "Time Out, the target has not answered"
    elif Status == 0x02:
        return "A CRC error has been detected by the CIU"
    elif Status == 0x03:
        return "A Parity error has been detected by the CIU"
    elif Status == 0x04:
        return "During an anticollision/select operation (ISO/IEC14443-3 Type A and ISO/IEC18092 106 kbps passive mode), an erroneous Bit Count has been detected"
    elif Status == 0x05:    
        return "Framing error during mifare operation"
    elif Status == 0x06:
        return "An abnormal bit-collision has been detected during bit wise anticollision at 106 kbps"
    elif Status == 0x07:
        return "Communication buffer size insufficient"
    elif Status == 0x09:
        return "RF Buffer overflow has been detected by the CIU (bit BufferOvfl of the register CIU_ERROR)"
    elif Status == 0x0A:
        return "In active communication mode, the RF field has not been switched on in time by the counterpart (as defined in NFCIP-1 standard)"
    elif Status == 0x0B:
        return "RF Protocol error (cf. [4], description of the CIU_ERROR register)"
    elif Status == 0x0D:
        return "Temperature error: the internal temperature sensor has detected overheating, and therefore has automatically switched off the antenna drivers"
    elif Status == 0x0E:
        return "Internal buffer overflow"
    elif Status == 0x10:
        return "Invalid parameter (range, format, ...)"
    elif Status == 0x12:
        return "DEP Protocol: The PN532 configured in target mode does not support the command received from the initiator (the command received is not one of the following: ATR_REQ, WUP_REQ, PSL_REQ, DEP_REQ, DSL_REQ, RLS_REQ [1])."
    elif Status == 0x13:
        return "DEP Protocol, mifare or ISO/IEC14443-4: The data format does not match to the specification. Depending on the RF protocol used, it can be: BadlengthofRFreceivedframe,Incorrect value of PCB or PFB,InvalidorunexpectedRFreceivedframe, NADorDIDincoherence."
    elif Status == 0x14:
        return "mifare: Authentication error"
    elif Status == 0x23:
        return "ISO/IEC14443-3: UID Check byte is wrong"
    elif Status == 0x25:
        return "DEP Protocol: Invalid device state, the system is in a state which does not allow the operation"
    elif Status == 0x26:
        return "Operation not allowed in this configuration (host controller interface)"
    elif Status == 0x27:
        return "This command is not acceptable due to the current context of the PN532 (Initiator vs. Target, unknown target number, Target not in the good state, ...)"
    elif Status == 0x29:
        return "The PN532 configured as target has been released by its initiator"
    elif Status == 0x2A:
        return "PN5321 and ISO/IEC14443-3B only: the ID of the card does not match, meaning that the expected card has been exchanged with another one."
    elif Status == 0x2B:
        return "PN5321 and ISO/IEC14443-3B only: the card previously activated has disappeared."
    elif Status == 0x2C:
        return "Mismatch between the NFCID3 initiator and the NFCID3 target in DEP 212/424 kbps passive."
    elif Status == 0x2D:
        return "An over-current event has been detected"
    elif Status == 0x2E:
        return "NAD missing in DEP frame"
    else:
        return "unknwon status"


def pn532ParseAnswer(Answer):
    if len(Answer) < 2:
        return "empty answer"
        
    if Answer[0] != 0xD5:
        return "invalid answer header"
    
    if Answer[1] == 0x03:
        if len(Answer) != 6:
            return "invalid answer"
        
        return "IC = %x, Ver = %x, Rev = %x,"%(Answer[2],Answer[3],Answer[4])+" ISO18092 initiator support = "+str(Answer[5]&0x08)+" ISO18092 target support = "+str(Answer[5]&0x04)+" ISO/IEC 14443 TypeB = "+str(Answer[5]&0x02)+" ISO/IEC 14443 TypeA = "+str(Answer[5]&0x01)
    

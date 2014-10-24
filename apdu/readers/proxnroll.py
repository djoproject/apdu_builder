#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2014 Jonathan Delvaux <apdu@djoproject.net>

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

from apdu.standard.iso7816_4 import iso7816_4APDUBuilder
from apdu.misc.apdu import ApduDefault
from apdu.misc.util import getPIXSS, getPIXNN
from apdu.misc.exception import apduBuilderException,apduAnswserException
from apdu.library.pcsc import pcscAPDUBuilder

class ProxnrollAPDUBuilder(pcscAPDUBuilder):
    proxnrollSW = {
        0x62:{0x82: "End of data reached before Le bytes (Le is greater than data length)"},
        0x63:{0x00: "Error reported by the contactless interface (when high-order bit of P2 is 1)."},
        0x67:{0x00: "Wrong length (Lc incoherent)"},
        0x68:{0x00: "CLA byte is not correct"},
        0x69:{0x81: "Command incompatible",
              0x82: "Security status not satisfied or CRYPTO1 authentication failed",
              0x86: "Volatile memory is not available or key type is not valid",
              0x87: "Non-volatile memory is not available",
              0x88: "Key number is not valid",
              0x89: "Key length is not valid"},
        0x6A:{0x81: "Function not supported (INS byte is not correct), or not available for the selected PICC/VICC",
              0x82: "Wrong address (no such block or no such offset in the PICC/VICC)",
              0x84: "Wrong length (trying to write too much data at once)"},
        0x6B:{0x00: "Wrong parameter P1 or/and P2"},
        0x6C:{None: "Wrong length (Le is shorter than data length, XX in SW2 gives the correct value)"},
        0x6F:{0x00: "No answer received (no card in the field, or card is mute)",
              0x01: "PICC/VICC mute or removed during the transfer", #TODO give a hint, maybe slow down the process or increase timeout in transmit
              0x02: "CRC error in card's answer",
              0x04: "Card authentication failed",
              0x05: "Parity error in card's answer",
              0x06: "Invalid card response opcode",
              0x07: "Bad anti-collision sequence",
              0x08: "Card's serial number is invalid",
              0x09: "Card or block locked",
              0x0A: "Card operation denied, must be authenticated first",
              0x0B: "Wrong number of bits in card's answer",
              0x0C: "Wrong number of bytes in card's answer",
              0x0D: "Card counter error",
              0x0E: "Card transaction error",
              0x0F: "Card write error",
              0x10: "Card counter increment error",
              0x11: "Card counter decrement error",
              0x12: "Card read error",
              0x13: "RC: FIFO overflow",
              0x15: "Framing error in card's answer",
              0x16: "Card access error",
              0x17: "RC: unknown opcode",
              0x18: "A collision has occurred",
              0x19: "RC: command execution failed",
              0x1A: "RC: hardware failure",
              0x1B: "RC: timeout",
              0x1C: "Anti-collision not supported by the card(s)",
              0x1F: "Bad card status",
              0x20: "Card: vendor specific error",
              0x21: "Card: command not supported",
              0x22: "Card: format of command invalid",
              0x23: "Card: option of command invalid",
              0x24: "Card: other error",
              0x3C: "Reader: invalid parameter",
              0x64: "Reader: invalid opcode",
              0x70: "Reader: internal buffer overflow",
              0x7D: "Reader: invalid length",
              0xE7: "SAM didn't answer with 9000 (maybe this is not a Calypso SAM !)",
              None: "Error code returned by the Gemcore"}}
    
    ##

    colorOFF   = 0x00
    colorON    = 0x01
    colorSLOW  = 0x02
    colorAUTO  = 0x03
    colorQUICK = 0x04
    colorBEAT  = 0x05
    
    ColorSettings = {"colorOFF"  :colorOFF,
                     "colorON"   :colorON,
                     "colorSLOW" :colorSLOW,
                     "colorAUTO" :colorAUTO,
                     "colorQUICK":colorQUICK,
                     "colorBEAT" :colorBEAT}

    ##
    
    protocolType_ISO14443_TCL         = 0x00
    protocolType_ISO14443A            = 0x01
    protocolType_ISO14443B            = 0x02
    protocolType_ISO15693             = 0x04
    protocolType_ISO15693_WithUID     = 0x05
    protocolType_ISO14443A_WithoutCRC = 0x09
    protocolType_ISO14443B_WithoutCRC = 0x0A
    protocolType_ISO15693_WithoutCRC  = 0x0C
    
    protocolType = {"ISO14443_TCL"        :protocolType_ISO14443_TCL,  #TODO be named 14443_default
                    "ISO14443A"           :protocolType_ISO14443A,
                    "ISO14443B"           :protocolType_ISO14443B,
                    "ISO15693"            :protocolType_ISO15693, #TODO be named 15693_default
                    "ISO15693_WithUID"    :protocolType_ISO15693_WithUID,
                    "ISO14443A_WithoutCRC":protocolType_ISO14443A_WithoutCRC,
                    "ISO14443B_WithoutCRC":protocolType_ISO14443B_WithoutCRC,
                    "ISO15693_WithoutCRC" :protocolType_ISO15693_WithoutCRC}
    
    ##
    
    lastByte_Complete_WithoutCRC  = 0x0F
    lastByte_With1bits_WithoutCRC = 0x1F
    lastByte_With2bits_WithoutCRC = 0x2F
    lastByte_With3bits_WithoutCRC = 0x3F
    lastByte_With4bits_WithoutCRC = 0x4F
    lastByte_With5bits_WithoutCRC = 0x5F
    lastByte_With6bits_WithoutCRC = 0x6F
    lastByte_With7bits_WithoutCRC = 0x7F
    
    lastByte = {"complete":lastByte_Complete_WithoutCRC,
                "1bits"   :lastByte_With1bits_WithoutCRC,
                "2bits"   :lastByte_With2bits_WithoutCRC,
                "3bits"   :lastByte_With3bits_WithoutCRC,
                "4bits"   :lastByte_With4bits_WithoutCRC,
                "5bits"   :lastByte_With5bits_WithoutCRC,
                "6bits"   :lastByte_With6bits_WithoutCRC,
                "7bits"   :lastByte_With7bits_WithoutCRC}
    
    ##
    
    redirectionToMainSlot = 0x80
    redirectionTo1stSlot  = 0x81
    redirectionTo2ndSlot  = 0x82
    redirectionTo3rdSlot  = 0x83
    redirectionTo4stSlot  = 0x84
    
    redirection = {"MainSlot":redirectionToMainSlot,
                   "1stSlot" :redirectionTo1stSlot,
                   "2ndSlot" :redirectionTo2ndSlot,
                   "3rdSlot" :redirectionTo3rdSlot,
                   "4stSlot" :redirectionTo4stSlot}
    
    ##
    
    timeoutDefault = 0x00
    timeout1ms     = 0x01
    timeout2ms     = 0x02
    timeout4ms     = 0x03
    timeout8ms     = 0x04
    timeout16ms    = 0x05
    timeout32ms    = 0x06
    timeout65ms    = 0x07
    timeout125ms   = 0x08
    timeout250ms   = 0x09
    timeout500ms   = 0x0A
    timeout1s      = 0x0B
    timeout2s      = 0x0C
    timeout4s      = 0x0D
    
    timeout = {"Default":timeoutDefault,
               "1ms"    :timeout1ms,
               "2ms"    :timeout2ms,
               "4ms"    :timeout4ms,
               "8ms"    :timeout8ms,
               "16ms"   :timeout16ms,
               "32ms"   :timeout32ms,
               "65ms"   :timeout65ms,
               "125ms"  :timeout125ms,
               "250ms"  :timeout250ms,
               "500ms"  :timeout500ms,
               "1s"     :timeout1s,
               "2s"     :timeout2s,
               "4s"     :timeout4s}

    ###################

    @staticmethod
    def getErrorMessageFromSW(sw1,sw2):
        if sw1 in ProxnrollAPDUBuilder.proxnrollSW and sw2 in ProxnrollAPDUBuilder.proxnrollSW[sw1]:
            return ProxnrollAPDUBuilder.proxnrollSW[sw1][sw2]
    
        return "unknown error, sw1="+str(sw1)+" sw2="+str(sw2)  
    
    @staticmethod
    def setLedColorFun(red,green,yellow_blue = None):        
        if red < 0 or red > 5:
            raise apduBuilderException("invalid argument red, a value between 0 and 5 was expected, got "+str(red))
            
        if green < 0 or green > 5:
            raise apduBuilderException("invalid argument green, a value between 0 and 5 was expected, got "+str(green))
        
        if yellow_blue == None:
            d = [0x1E,red,green]
        else:
            if yellow_blue < 0 or yellow_blue > 5:
                raise apduBuilderException("invalid argument yellow_blue, a value between 0 and 5 was expected, got "+str(yellow_blue))
            d = [0x1E,red,green,yellow_blue]
        
        return ApduDefault(cla=0xFF,ins=0xF0,p1=0x00,p2=0x00,data=d)
    
    @staticmethod    
    def setBuzzerDuration(duration):
        if duration < 0 or duration > 60000:
            raise apduBuilderException("invalid argument duration, a value between 0 and 60000 was expected, got "+str(duration))
        
        lsb = duration&0xFF
        msb = (duration>>8)&0xFF
        
        return ApduDefault(cla=0xFF,ins=0xF0,p1=0x00,p2=0x00,data=[0x1C,msb,lsb])
    
    @staticmethod    
    def test(expected_answer_size = 0,delay_to_answer=0, datas = []):
        
        if expected_answer_size < 0 or expected_answer_size > 255:
            raise apduBuilderException("invalid argument expected_answer_size, a value between 0 and 255 was expected, got "+str(expected_answer_size))
            
        if delay_to_answer < 0 or delay_to_answer > 63:
            raise apduBuilderException("invalid argument delay_to_answer, a value between 0 and 63 was expected, got "+str(delay_to_answer))
            
        if len(datas) < 0 or len(datas) > 255:
            raise apduBuilderException("invalid argument datas, a value list of length 0 to 255 was expected, got "+str(len(datas)))
        
        return ApduDefault(cla=0xFF,ins=0xFD,p1=expected_answer_size,p2=delay_to_answer,data=datas)

    #FIXME : avec un mauvais protocole, le reader renvoit 0x6f 0x47, code non defini...
    #           et ca renvoit 0x6f 0x01 quand ca reussi avec les ultralight...
    @staticmethod
    def encapsulate(datas,protocolType=0x00,timeoutType=0x00,defaultSW = True):
        
        if len(datas) < 1 or len(datas) > 255:
            raise apduBuilderException("invalid data size, a value between 1 and 255 was expected, got "+str(len(datas)))
        
        if timeoutType < 0 or timeoutType > 0x0D:
            raise apduBuilderException("invalid argument timeoutType, a value between 0 and 13 was expected, got "+str(timeoutType))
            
        if protocolType != 0x00 and protocolType != 0x01 and protocolType != 0x02 and protocolType != 0x04 and protocolType != 0x05 and protocolType != 0x09 and protocolType != 0x0A and protocolType != 0x0C and protocolType != 0x0F and protocolType != 0x1F and protocolType != 0x2F and protocolType != 0x3F and protocolType != 0x4F and protocolType != 0x5F and protocolType != 0x6F and protocolType != 0x7F and protocolType != 0x80 and protocolType != 0x81 and protocolType != 0x82 and protocolType != 0x83 and protocolType != 0x84:
            raise apduBuilderException("invalid argument protocolType, see the documentation")
            
        if not defaultSW:
            timeoutType &= 0x80
            
        return ApduDefault(cla=0xFF,ins=0xFE,p1=protocolType,p2=timeoutType,data=datas)
        
    ###
    @staticmethod
    def getDataCardCompleteIdentifier():
        return iso7816_4APDUBuilder.getDataCA(0xF0,0x00)
    
    @staticmethod
    def getDataCardType():
        return iso7816_4APDUBuilder.getDataCA(0xF1,0x00)

    @staticmethod
    def parseDataCardType(toParse):
        if len(toParse) != 3:
            raise apduAnswserException("(proxnroll) parseDataCardType, 3 bytes waited, got "+str(len(toParse)))
        
        print "Procole : "+getPIXSS(toParse[0]) + ", Type : " +getPIXNN((toParse[1] << 8) + toParse[2])  

    @staticmethod
    def getDataCardShortSerialNumber():
        return iso7816_4APDUBuilder.getDataCA(0xF2,0x00)

    @staticmethod
    def getDataCardATR():
        return iso7816_4APDUBuilder.getDataCA(0xFA,0x00)
    
    @staticmethod
    def getDataProductSerialNumber():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x00)

    @staticmethod
    def getDataHarwareIdentifier():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x01)

    @staticmethod
    def getDataVendorName():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x81)

    @staticmethod
    def getDataProductName():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x82)

    @staticmethod
    def getDataProductSerialNumber():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x83)

    @staticmethod
    def getDataProductUSBIdentifier():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x84)
        
    @staticmethod
    def getDataProductVersion():
        return iso7816_4APDUBuilder.getDataCA(0xFF,0x85)
        
    ###          
    
    @staticmethod
    def loadKey(KeyIndex,Key,InVolatile = True ,isTypeA = True):
        #only allow mifare key
        if len(Key) != 6:
            raise apduBuilderException("invalid key length, must be 6, got "+str(len(Key)))

        #proxnroll specific params
        if InVolatile:
            if KeyIndex < 0 or KeyIndex > 3:
                raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 3 was expected, got "+str(KeyIndex))
        else:
            if KeyIndex < 0 or KeyIndex > 15:
                raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 15 was expected, got "+str(KeyIndex))
        
        #B key special index
        if not isTypeA:
            KeyIndex &= 0x10
            
        return pcscAPDUBuilder.loadKey(KeyIndex,Key,InVolatile)
        
    @staticmethod
    def generalAuthenticate(blockNumber,KeyIndex,InVolatile = True ,isTypeA = True):
        if blockNumber < 0 or blockNumber > 255:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        if InVolatile:
            if KeyIndex < 0 or KeyIndex > 3:
                raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 3 was expected, got "+str(KeyIndex))
            
            #volatile key special index
            KeyIndex &= 0x20
        else:
            if KeyIndex < 0 or KeyIndex > 15:
                raise apduBuilderException("invalid argument KeyIndex, a value between 0 and 15 was expected, got "+str(KeyIndex))

        ap = pcscAPDUBuilder.generalAuthenticate(blockNumber,KeyIndex,InVolatile,isTypeA)        
        ap.setIns(0x88)
     
        return ap
        
    @staticmethod
    def mifareClassicRead(blockNumber,Key = None):
        if blockNumber < 0 or blockNumber > 255:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))
        
        if Key == None:
            return ApduDefault(cla=0xFF,ins=0xF3,p1=0x00,p2=blockNumber)
        else:
            if len(Key) != 6:
                raise apduBuilderException("invalid key length, must be 6, got "+str(len(Key)))
                
            return ApduDefault(cla=0xFF,ins=0xF3,p1=0x00,p2=blockNumber,data=Key)
        
    @staticmethod
    def mifareClassifWrite(blockNumber,datas,Key = None):
        if blockNumber < 0 or blockNumber > 255:
            raise apduBuilderException("invalid argument blockNumber, a value between 0 and 255 was expected, got "+str(blockNumber))

        if len(datas) < 1 or len(datas) > 255:
            raise apduBuilderException("invalid datas size, must be a list from 1 to 255 item, got "+str(len(datas)))
            
        if (len(datas) % 16) != 0:
            raise apduBuilderException("invalid datas size, must be a multiple of 16")

        if Key == None:
            return ApduDefault(cla=0xFF,ins=0xF4,p1=0x00,p2=blockNumber,data=datas)
        else:
            if len(Key) != 6:
                raise apduBuilderException("invalid key length, must be 6, got "+str(len(Key)))
            
            toSend = []
            toSend.extend(datas)
            toSend.extend(Key)
            return ApduDefault(cla=0xFF,ins=0xF4,p1=0x00,p2=blockNumber,data=toSend)
        
    
    #### SLOT CONTROL ####
    @staticmethod
    def slotControlResumeCardTracking():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x00,p2=0x00)
    
    @staticmethod
    def slotControlSuspendCardTracking():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x01,p2=0x00)
    
    @staticmethod
    def slotControlStopRFField():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x10,p2=0x00)

    @staticmethod
    def slotControlStartRFField():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x10,p2=0x01)
    
    @staticmethod
    def slotControlResetRFField():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x10,p2=0x02)
        
    @staticmethod
    def slotControlTCLDeactivation():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x00)

    @staticmethod
    def slotControlTCLActivationTypeA():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x01)

    @staticmethod
    def slotControlTCLActivationTypeB():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x02)
    
    @staticmethod
    def slotControlDisableNextTCL():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x04)

    @staticmethod
    def slotControlDisableEveryTCL():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x05)

    @staticmethod
    def slotControlEnableTCLAgain():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x06)

    @staticmethod
    def slotControlResetAfterNextDisconnectAndDisableNextTCL():
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0x20,p2=0x07)
    
    @staticmethod
    def slotControlStop():
        "stop the slot"
        return ApduDefault(cla=0xFF,ins=0xFB,p1=0xDE,p2=0xAD)
    
    #### CALYPSO METHOD ###
    
    @staticmethod
    def configureCalypsoSamSetSpeed9600():
        return ApduDefault(cla=0xFF,ins=0xFC,p1=0x04,p2=0x00)
        
    @staticmethod
    def configureCalypsoSamSetSpeed115200():
        return ApduDefault(cla=0xFF,ins=0xFC,p1=0x04,p2=0x01)

    @staticmethod
    def configureCalypsoSamEnableInternalDigestUpdate():
        return ApduDefault(cla=0xFF,ins=0xFC,p1=0x08,p2=0x00)
        
    @staticmethod
    def configureCalypsoSamDisableInternalDigestUpdate():
        return ApduDefault(cla=0xFF,ins=0xFC,p1=0x08,p2=0x01)
        




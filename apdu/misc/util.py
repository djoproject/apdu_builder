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

import commands
import random
import binascii
import os

#TODO utilisation d'exception inexistante...

def printHexaTableWithoutSpace(l):
    return ''.join( [ "%02X" % x for x in l ] ).strip()

def stringToHex(string ):
    ret = []

    for i in range(0, len(string)/2):
        ret.extend([int( str(string[(i*2)]+string[(i*2)+1]) , 16  )])

    return ret

def xorList(list1, list2):
    if len(list1) != len(list2):
        raise ParamException("(myutil) xorList, the lists to xor have different size")

    ret = []
    for i in range(0,len(list1)):
        ret.append(list1[i] ^ list2[i])

    return ret

def sslDesDecToReader(challenge,key):
    if len(challenge) % 8 != 0:
        raise CypherException("sslDesDecToReader, challenge size isn't a multiple of 8")

    iv = [0,0,0,0,0,0,0,0]

    if len(key) == 8:
        cmd = " | xxd -p -r | openssl enc -des -d -K "+printHexaTableWithoutSpace(key)+" -iv 0 -nopad | xxd -p"
    elif len(key) == 16:
        cmd = " | xxd -p -r | openssl enc -des3 -d -K "+printHexaTableWithoutSpace(key)+printHexaTableWithoutSpace(key[:8])+" -iv 0 -nopad | xxd -p"
    else:
        raise CypherException("sslDesDecToReader, key size is different of 8 or 16")

    count = 0
    ret = []
    while count < len(challenge):
        rep = commands.getstatusoutput("echo "+printHexaTableWithoutSpace(xorList(challenge[count:(count+8)], iv))+cmd)

        try:
            iv = stringToHex(rep[1])
        except ValueError:
            raise CypherException("sslDesDecToReader, an error has occur in openssl call : "+str(rep))
            
        ret.extend(iv)
        count += 8
    
    return ret

def sslDesDecFromReader(challenge,key):
    if len(challenge) % 8 != 0:
        raise CypherException("sslDesDecFromReader, challenge size isn't a multiple of 8")

    if len(key) == 8:
        cmd = " | xxd -p -r | openssl enc -des -d -K "+printHexaTableWithoutSpace(key)+" -iv 0 -nopad | xxd -p"
    elif len(key) == 16:
        cmd = " | xxd -p -r | openssl enc -des3 -d -K "+printHexaTableWithoutSpace(key)+printHexaTableWithoutSpace(key[:8])+" -iv 0 -nopad | xxd -p"
    else:
        raise CypherException("sslDesDecFromReader, key size is different of 8 or 16")
        
    iv = [0,0,0,0,0,0,0,0]
    ret = []
    count = 0
    
    while (count < len(challenge)):
        rep = commands.getstatusoutput("echo "+printHexaTableWithoutSpace(challenge[count:(count+8)])+cmd)

        if rep[0] != 0:
            raise CypherException("sslDesDecFromReader, an error has occur in openssl call : "+str(rep[1]))

        try:
            ret.extend(xorList(stringToHex(rep[1]), iv))
        except ValueError:
            raise CypherException("sslDesDecFromReader, an error has occur in openssl call : "+str(rep[1]))
            
        iv = challenge[count:(count+8)]
        count += 8
    
    return ret
    
def getNounce(size = 8):
    ret = []
    if os.path.exists("/dev/random"):
        #print "/dev/random used"
        f = open("/dev/random","r")
        for v in f.read(size):
            ret.append(int(binascii.hexlify(v), 16))
        f.close()
    elif os.path.exists("/dev/urandom"):
        print "warning, /dev/urandom used"
        f = open("/dev/urandom","r")
        for v in f.read(size):
            ret.append(int(binascii.hexlify(v), 16))
        f.close()
    else:
        print "warning, python random used"
        for i in range(0,size):
            ret.append(random.randint(0,255))
            
    return ret

def generateD1D2(NT, nounce, key):    
    #calcul ntprime
    NTprime = []
    NTprime.extend(NT)
    NTprime.append(NTprime.pop(0))

    #calcul d1
    D1 = sslDesDecToReader(nounce,key)

    #calcul d2
    D1xorNTprime = []
    for i in range(0,8):
        D1xorNTprime.append(D1[i] ^ NTprime[i])

    D2 = sslDesDecToReader(D1xorNTprime,key)

    #challenge step 2
    rep = D1
    rep.extend(D2)

    return rep
    
def computeCRC(listByte):
    wCrc = 0x6363
    for i in range(0, len(listByte)):
        bt = listByte[i]
        bt = (bt ^ (wCrc & 0xff)) & 0xff
        bt = (bt ^ (bt << 4)) & 0xff
        wCrc = ((wCrc >> 8) ^ (bt << 8) ^ (bt << 3) ^ (bt >> 4)) & 0xffff

    return wCrc & 0x00ff, (wCrc >> 8) & 0x00ff

def getPIXSS(value):
    if (value == 0x00): return "No Information given"
    elif (value == 0x01): return "ISO 14443 A, level 1"
    elif (value == 0x02): return "ISO 14443 A, level 2"
    elif (value == 0x03): return "ISO 14443 A, level 3 or 4 (and Mifare)"
    elif (value == 0x04): return "RFU"
    elif (value == 0x05): return "ISO 14443 B, level 1"
    elif (value == 0x06): return "ISO 14443 B, level 2"
    elif (value == 0x07): return "ISO 14443 B, level 3 or 4"
    elif (value == 0x08): return "RFU"
    elif (value == 0x09): return "ISO 15693, level 1"
    elif (value == 0x0A): return "ISO 15693, level 2"
    elif (value == 0x0B): return "ISO 15693, level 3"
    elif (value == 0x0C): return "ISO 15693, level 4"
    elif (value == 0x0D): return "Contact (7816-10) I2C"
    elif (value == 0x0E): return "Contact (7816-10) Extended I2C"
    elif (value == 0x0F): return "Contact (7816-10) 2WBP"
    elif (value == 0x10): return "Contact (7816-10) 3WBP"
    elif (value == 0xF0): return "ICODE EPC"
    else: return "Unknonw Value %.x"%value
    
def getPIXNN(value):
    if (value == 0x0001): return "NXP Mifare Standard 1k"
    elif (value == 0x0002): return "NXP Mifare Standard 4k"
    elif (value == 0x0003): return "NXP Mifare UltraLight"
    elif (value == 0x0004): return "SLE55R_XXXX"
    elif (value == 0x0006): return "ST MicroElectronics SR176"
    elif (value == 0x0007): return "ST MicroElectronics SRIX4K"
    elif (value == 0x0008): return "AT88RF020"
    elif (value == 0x0009): return "AT88SC0204CRF"
    elif (value == 0x000A): return "AT88SC0808CRF"
    elif (value == 0x000B): return "AT88SC1616CRF"
    elif (value == 0x000C): return "AT88SC3216CRF"
    elif (value == 0x000D): return "AT88SC6416CRF"
    elif (value == 0x000E): return "SRF55V10P"
    elif (value == 0x000F): return "SRF55V02P"
    elif (value == 0x0010): return "SRF55V10S"
    elif (value == 0x0011): return "SRF55V02S"
    elif (value == 0x0012): return "Texas Instruments TAG IT"
    elif (value == 0x0013): return "LRI512"
    elif (value == 0x0014): return "NXP ICODE SLI"
    elif (value == 0x0015): return "TEMPSENS"
    elif (value == 0x0016): return "NXP ICODE 1"
    elif (value == 0x0017): return "PicoPass 2K"
    elif (value == 0x0018): return "PicoPass 2KS"
    elif (value == 0x0019): return "PicoPass 16K"
    elif (value == 0x001A): return "PicoPass 16Ks"
    elif (value == 0x001B): return "PicoPass 16K(8x2)"
    elif (value == 0x001C): return "PicoPass 16KS(8x2)"
    elif (value == 0x001D): return "PicoPass 32KS(16+16)"
    elif (value == 0x001E): return "PicoPass 32KS(16+8x2)"
    elif (value == 0x001F): return "PicoPass 32KS(8x2+16)"
    elif (value == 0x0020): return "PicoPass 32KS(8x2+8x2)"
    elif (value == 0x0021): return "ST MicroElectronics LRI64"
    elif (value == 0x0022): return "NXP ICODE UID"
    elif (value == 0x0023): return "NXP ICODE EPC"
    elif (value == 0x0024): return "LRI12"
    elif (value == 0x0025): return "LRI128"
    elif (value == 0x0026): return "Mifare Mini"
    elif (value == 0x0027): return "my-d move (SLE 66R01P)"
    elif (value == 0x0028): return "my-d NFC (SLE 66RxxP)"
    elif (value == 0x0029): return "my-d proximity 2 (SLE 66RxxS)"
    elif (value == 0x002A): return "my-d proximity enhanced (SLE 55RxxE)"
    elif (value == 0x002B): return "my-d light (SRF 55V01P)"
    elif (value == 0x002C): return "PJM Stack Tag (SRF 66V10ST)"
    elif (value == 0x002D): return "PJM Item Tag (SRF 66V10IT)"
    elif (value == 0x002E): return "PJM Light (SRF 66V01ST)"
    elif (value == 0x002F): return "Jewel Tag"
    elif (value == 0x0030): return "Topaz NFC Tag"
    elif (value == 0x0031): return "AT88SC0104CRF"
    elif (value == 0x0032): return "AT88SC0404CRF"
    elif (value == 0x0033): return "AT88RF01C"
    elif (value == 0x0034): return "AT88RF04C"
    elif (value == 0x0035): return "i-Code SL2"
    elif (value == 0xFFA0): return "Unidentified 14443 A card"
    elif (value == 0xFFB0): return "Unidentified 14443 B card"
    elif (value == 0xFFB1): return "ASK CTS 256B"
    elif (value == 0xFFB2): return "ASK CTS 512B"
    elif (value == 0xFFB3): return "ST MicroElectronics SRI 4K"
    elif (value == 0xFFB4): return "ST MicroElectronics SRI X512"
    elif (value == 0xFFB5): return "ST MicroElectronics SRI 512"
    elif (value == 0xFFB6): return "ST MicroElectronics SRT 512"
    elif (value == 0xFFB7): return "PICOTAG"
    elif (value == 0xFFC0): return "Calypso card using the Innovatron protocol"
    elif (value == 0xFFD0): return "Unidentified 15693 card"
    elif (value == 0xFFD1): return "Unidentified 15693 Legic card"
    elif (value == 0xFFD2): return "Unidentified 15693 ST MicroElectronics card"
    elif (value == 0xFFE1): return "NXP ICODE UID-OTP"
    elif (value == 0xFFE2): return "Unidentified EPC card"
    elif (value == 0xFFFF): return "Virtual card (test only)"
    else: return "Unknonw Value %.x"%value

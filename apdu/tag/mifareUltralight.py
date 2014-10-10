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
    #authentication for ultraligh C
    #change key, auth settings, ...

from apdu.misc.apdu import Apdu
from apdu.misc.exception import apduBuilderException

class ApduMifareUltralight(Apdu):
    def __init__(self,ins,param,data = []):
        self.extend([ins,param])
        if len(data) > 0:
            self.extend(data)

class MifareUltralightAPDUBuilder(object):
    
    @staticmethod
    def REQA():
        pass #TODO
        
    @staticmethod
    def WUPA():
        pass #TODO
    
    @staticmethod
    def Anticollision_level1():
        pass #TODO

    @staticmethod
    def Select_level1():
        pass #TODO
        
    @staticmethod
    def Anticollision_level2():
        pass #TODO

    @staticmethod
    def Select_level2():
        pass #TODO
    
    @staticmethod
    def Halt():
        return ApduMifareUltralight(ins=0x50,param=0x00)
    
    @staticmethod
    def readSector(address=0):
        if address < 0 or address > 0x0F:
            raise apduBuilderException("invalid argument address, a value between 0 and 15 was expected, got "+str(address))
        
        return ApduMifareUltralight(ins=0x30,param=(address&0xFF))
    
    @staticmethod
    def writeSector(datas, address=0):
        if address < 0 or address > 0x0F:
            raise apduBuilderException("invalid argument address, a value between 0 and 15 was expected, got "+str(address))
        
        if len(datas) != 4:
            raise apduBuilderException("invalid datas size, must be a list with 4 item, got "+str(len(datas)))
        
        return ApduMifareUltralight(ins=0xA2,param=(address&0xFF),data=datas)
    
    @staticmethod
    def CompatibilityWrite(datas, address=0):
        if address < 0 or address > 0x0F:
            raise apduBuilderException("invalid argument address, a value between 0 and 15 was expected, got "+str(address))
        
        if len(datas) != 4:
            raise apduBuilderException("invalid datas size, must be a list with 4 item, got "+str(len(datas)))
        
        datas.extend([0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
        
        return ApduMifareUltralight(ins=0xA0,param=(address&0xFF),data=datas)
            








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
    
    TYPE_AUTO           = 0x00
    TYPE_I2C_1KTO16K    = 0x01
    TYPE_I2C_32KTO1024K = 0x02
    TYPE_AT88SC153      = 0x3
    TYPE_AT88SC1608     = 0x4
    TYPE_SLE4418_4428   = 0x5
    TYPE_SLE4432_4442   = 0x6
    TYPE_SLE4406_4436_5536  = 0x7
    TYPE_SLE4404            = 0x8
    TYPE_AT88SC101_102_1003 = 0x9
    #TYPE_ = 0xA
    #TYPE_ = 0xB
    TYPE_MCU_T0 = 0xC
    TYPE_MCU_T1 = 0xD
    
    @staticmethod
    def getReaderInformation():
        return ApduDefault(cla=0xFF,ins=0x09,p1=0x00,p2=0x00,expected_answer=0x10)
    
    @staticmethod
    def selectType(TYPE = 0):
        if TYPE < 0 or TYPE > 0xD:
            raise apduBuilderException("invalid argument TYPE, a value between 0 and 13 was expected, got "+str(TYPE))
        
        return ApduDefault(cla=0xFF,ins=0xA4,p1=0x00,p2=0x00,data=[TYPE])
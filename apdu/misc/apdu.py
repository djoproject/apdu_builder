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

from string import rstrip

class ApduBuilder(object):

    @staticmethod
    def getErrorMessageFromSW(sw1,sw2):
        return "unknown error, sw1="+str(sw1)+" sw2="+str(sw2)    
    
    

PACK = 1
HEX = 2
UPPERCASE = 4
COMMA = 8

def toHexString(bytes=[], format=0):
    for byte in tuple(bytes): 
        pass 

    if not isinstance(bytes,list): 
        raise TypeError, 'not a list of bytes' 

    if bytes == None or bytes == []: 
        return "" 
    else: 
        pformat = "%-0.2X" 
        if COMMA & format: 
            pformat = pformat + "," 
        pformat = pformat + " " 
        if PACK & format: 
            pformat = rstrip(pformat) 
        if HEX & format: 
            if UPPERCASE & format: 
                pformat = "0X" + pformat 
            else: 
                pformat = "0x" + pformat 
                    
        return rstrip(rstrip(reduce(lambda a, b: a + pformat % ((b + 256) % 256), [""] + bytes)), ',')

#
# this class is an abstract prototype to all apdu sent to any card reader/writer
#
class Apdu(list):
    "apdu abstract class"
    #def __init__(self):
    #    pass
        
    def getSize(self):
        "return the length of the command"
        return len(self)
        
    def toHexArray(self):
        "return the command into a byte array"
        return self
    
    def __str__(self):
        return toHexString(self)
        
class ApduDefault(Apdu):
    "apdu abstract class"
    def __init__(self,cla,ins,p1=0,p2=0,data=[],expected_answer=0):
        self.extend([cla,ins,p1,p2])
        
        if len(data) > 0:
            self.append(len(data))
            self.extend(data)
        
        self.append(expected_answer)

    def setIns(ins):
        #TODO check the self size
        self[1] = ins

    #def getSize(self):
    #    "return the length of the command"
    #    return len(self.table)

    #def toHexArray(self):
    #    "return the command into a byte array"
    #    return self.table
        
class ApduRaw(Apdu):
    def __init__(self,rawByte):
        self.extend(rawByte)
        
    #def getSize(self):
    #    "return the length of the command"
    #    return len(self.rawByte)

    #def toHexArray(self):
    #    "return the command into a byte array"
    #    return self.rawByte
        
    #def __str__(self):
    #    return toHexString(self.table)
        


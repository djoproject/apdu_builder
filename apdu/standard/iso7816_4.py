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

from apdu.misc.apdu import ApduDefault, ApduBuilder

class iso7816_4APDUBuilder(ApduBuilder):

    @staticmethod
    def getDataCA(P1,P2):
        return ApduDefault(cla=0xFF,ins=0xCA,p1=P1,p2=P2)
    
    @staticmethod
    def getDataCB(P1,P2,Data):
        return ApduDefault(cla=0xFF,ins=0xCA,p1=P1,p2=P2, data=Data)

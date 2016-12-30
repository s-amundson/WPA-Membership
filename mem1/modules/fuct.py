#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import datetime

def calc_expire(edate):
    if(edate == None): edate = datetime.date.today() + datetime.timedelta(365)
    elif(edate > datetime.date.today()):
        edate = edate + datetime.timedelta(365)
    else: edate = datetime.date.today() + datetime.timedelta(365)
    return edate

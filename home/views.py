from django.shortcuts import render
from requests import request
import numpy as np

from home.models import *
from django.http import HttpResponseRedirect, JsonResponse

import threading

import pyupbit
import time
import pandas as pd
from home import auto_trade_thread as att

auto_trade_thread = att.auto_trade_thread
upbit = att.upbit

def home(request) :
    """
        전체 계좌 조회 Page
    """
    df = upbit.get_balances_tickers()
    qs = [vals for vals in df.to_dict('records')]
    data = {'data':qs}
    return render(request, 'home.html', data)

def onoff(request) :
    """
        Auto Trade Page
    """
    print("auto_trade_thread.isAlive() = ", auto_trade_thread.isAlive())
    status_chk = Status.objects.filter(id=1)
    data = {'chk':status_chk[0]}
    return render(request, 'onoff.html', data)

def changeStatus(request) :
    """
        Auto Trade Page
        Ajax
        thread on and off
    """
    global auto_trade_thread
    status = Status.objects.get(id=1)
    if request.POST.get('chk') == "True" :
        status.status_chk = False
        auto_trade_thread.start()
        print("auto_trade_thread.isAlive() = ", auto_trade_thread.isAlive())
    elif request.POST.get('chk') == "False" :
        status.status_chk = True
        auto_trade_thread.kill()
        auto_trade_thread = att.Worker()
        auto_trade_thread.daemon = True
    status.save()
    context = {"result" : "success"}
    return JsonResponse(context)

def insertFage(request) :
    return render(request, 'insertFage.html')

def insert(request) :
    hometest = Test()
    hometest.test_text = request.POST['text']
    hometest.save()
    return HttpResponseRedirect('/')

def dataDelete(request) :
    test = Test.objects.get(id=request.POST['id'])
    test.delete()
    return HttpResponseRedirect('/')
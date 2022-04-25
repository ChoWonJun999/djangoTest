from django.shortcuts import render
from requests import request
import numpy as np

from home.models import *
from django.http import HttpResponseRedirect, JsonResponse

import threading

import pyupbit
import time
import pandas as pd

def login() :
    """upbit 로그인"""
    access = "CR3vYIFTqY2bhXpJ8AU8OK8YrlDCwYq3dkutsHM4"
    secret = "PPPxxTjZG1LWPRqeTg5xoQGEsSVpr1DnqxUW1Qxx"

    upbit = pyupbit.Upbit(access, secret)
    return upbit
upbit = login()
print("upbit login")

def get_current_price(ticker):
    """현재 가격 가져오기"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
def get_balance(ticker) :
    """잔고 조회 및 가져오기"""
    balances = upbit.get_balances()

    for b in balances:
        if b['currency'] == ticker :
            if b['balance'] is not None :
                return float(b['balance'])
            else:
                return 0
def get_valuation_gain_loss(ticker) :
    """수익률"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker :
            if b['avg_buy_price'] is not None :
                return float(b['avg_buy_price'])
            else:
                return 0
def BB_1hour(ticker="KRW-BTC", cnt=20, k=2) :
    """1시간봉 볼린저 밴드"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=cnt+2)
    ma20 = pd.DataFrame(df['close'])
    ma20['mid'] = ma20['close'].rolling(window=cnt).mean()
    ma20['std'] = ma20['close'].rolling(window=cnt).std()
    ma20['upper'] = ma20['mid'] + (ma20['std'] * k)
    ma20['lower'] = ma20['mid'] - (ma20['std'] * k)
    ma20 = ma20.reset_index()
    return ma20
def BB_15minute(ticker="KRW-BTC", cnt=20, k=2) :
    """15분봉 볼린저 밴드"""
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=cnt+2)
    ma20 = pd.DataFrame(df['close'])
    ma20['mid'] = ma20['close'].rolling(window=cnt).mean()
    ma20['std'] = ma20['close'].rolling(window=cnt).std()
    ma20['upper'] = ma20['mid'] + (ma20['std'] * k)
    ma20['lower'] = ma20['mid'] - (ma20['std'] * k)
    ma20 = ma20.reset_index()
    return ma20
class Worker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        for i in 100 :
            print("i = ", i)
            time.sleep(1)
        ''' 
        ticker = "KRW-BTC"
        cnt = 20
        k = 2
        while True : 
            try :
                print("haha")
                schedule.run_pending()
                current_price = get_current_price(ticker)
                krw = get_balance("KRW")
                ticker_price = get_balance(ticker[4:])
                if krw > 5000 :
                    bbh = BB_1hour(ticker, cnt, k)
                    if bbh.iloc[21]['close'] < bbh.iloc[21]['lower'] * 0.985 and bbh.iloc[19]['close'] < bbh.iloc[19]['lower'] :
                        bbm = BB_15minute(ticker, cnt, k)
                        if bbm.iloc[21]['close'] < bbm.iloc[21]['lower'] * 0.985 and bbh.iloc[19]['close'] < bbh.iloc[19]['lower'] :
                            upbit.buy_market_order(ticker, krw*0.9999)
                elif int(current_price * get_balance(ticker[4:])) > 5000 :
                    if(current_price < get_valuation_gain_loss(ticker[4:])*1.015) :
                        upbit.sell_market_order(ticker, ticker_price*0.9995)
                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)
         '''
auto_trade_thread = Worker()
auto_trade_thread.daemon = True
print("auto_trade_thread 선언")

def home(request) :
    df = upbit.get_balances_tickers()
    qs = [vals for vals in df.to_dict('records')]
    data = {'data':qs}
    return render(request, 'home.html', data)

def onoff(request) :
    status_chk = Status.objects.filter(id=1)
    data = {'chk':status_chk[0]}
    return render(request, 'onoff.html', data)

def changeStatus(request) :
    status = Status.objects.get(id=1)
    if request.POST.get('chk') == "True" :
        status.status_chk = False
        # auto_trade_thread.start()
    elif request.POST.get('chk') == "False" :
        status.status_chk = True
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
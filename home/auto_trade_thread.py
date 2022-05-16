import threading
import time
import schedule
import pyupbit
import pandas as pd
import datetime

class Worker(threading.Thread) :
    """
        thread
    """
    def __init__(self, _upbit, _method):
        super().__init__()
        self._kill = threading.Event()
        self.chk = True
        self.ticker = "KRW-BTC"
        self._upbit = _upbit
        self._method = _method

    def run(self):
        """
            thread start

            self._method
            db에서 id 가져오는거 주의
            테이터 변동 시 id 맞춰 줘야함
        """
        self.chk = True
        while self.chk : 
            if self._method == 1 :
                aVolatilityStrategy(self.ticker, self._upbit)
            elif self._method == 2 :
                bollingerBand(self.ticker, self._upbit)
            elif self._method == 3 :
                fiveTen(self.ticker, self._upbit)
        
    def kill(self) :
        self.chk = False
        self._kill.set()

def aVolatilityStrategy(_ticker, _upbit) :
    """ 변동성 전략 """
    try:
        print("변동성 전략")
        now = datetime.datetime.now()
        start_time = get_start_time(_ticker)
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(_ticker, 0.5)
            current_price = get_current_price(_ticker)
            if target_price < current_price :
                krw = get_balance(_upbit, "KRW")
                if krw > 5000:
                    _upbit.buy_market_order(_ticker, krw*0.9995)
        else:
            ticker_price = get_balance(_upbit, _ticker[4:])
            if int(current_price * ticker_price) > 5000:
                _upbit.sell_market_order(_ticker, ticker_price*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

def bollingerBand(_ticker, _upbit) :
    """ 볼린저 밴드 """
    cnt = 20
    k = 2
    try :
        print("볼린저 밴드")
        schedule.run_pending()
        current_price = get_current_price(_ticker)
        krw = get_balance(_upbit, "KRW")
        ticker_price = get_balance(_upbit, _ticker[4:])
        if krw > 5000 :
            bbh = BB_1hour(_ticker, cnt, k)
            if bbh.iloc[21]['close'] < bbh.iloc[21]['lower'] * 0.985 and bbh.iloc[19]['close'] < bbh.iloc[19]['lower'] :
                bbm = BB_15minute(_ticker, cnt, k)
                if bbm.iloc[21]['close'] < bbm.iloc[21]['lower'] * 0.985 and bbh.iloc[19]['close'] < bbh.iloc[19]['lower'] :
                    _upbit.buy_market_order(_ticker, krw*0.9999)
        elif int(current_price * ticker_price) > 5000 :
            if(current_price < get_valuation_gain_loss(_upbit, _ticker[4:])*1.015) :
                _upbit.sell_market_order(_ticker, ticker_price*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

def fiveTen(_ticker, _upbit) :
    """ 5-10 """
    try : 
        print("5-10")
        schedule.run_pending()
        now = datetime.datetime.now()
        start_time = get_start_time(_ticker)

        if start_time < now < start_time + datetime.timedelta(minutes=1) and oneTime :
            krw = get_balance(_upbit, "KRW")
            btc = get_balance(_upbit, _ticker[4:])
            current_price = get_current_price(_ticker)
            if krw > 5000 :
                if chk(_ticker) :
                    _upbit.buy_market_order(_ticker, krw*0.9995)
                    oneTime = False
            elif btc > 0.00008 : 
                if chk(_ticker) == False :
                    _upbit.sell_market_order(_ticker, btc*0.9995)
                    oneTime = False
        else :
            oneTime = True
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

def chk(_ticker) :
    """ Ma(5) - Ma(10)"""
    df = pyupbit.get_ohlcv(_ticker, interval="minute10", count=11)
    df.head()
    df.tail()
    ma5 = df['close'].rolling(window=5).mean()
    ma10 = df['close'].rolling(window=10).mean()
    ma5 = ma5.reset_index()
    ma10 = ma10.reset_index()
    if ma5.iloc[-1]['close'] > ma10.iloc[-1]['close'] :
        return True
    else :
        return False
def get_target_price(ticker, k) :
    """매수 가격 설정"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
def get_start_time(ticker) :
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)

    start_time = df.index[0]
    return start_time
def get_current_price(ticker):
    """현재 가격 가져오기"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
def get_balance(_upbit, ticker) :
    """잔고 조회 및 가져오기"""
    balances = _upbit.get_balances()

    for b in balances:
        if b['currency'] == ticker :
            if b['balance'] is not None :
                return float(b['balance'])
            else:
                return 0
def get_valuation_gain_loss(_upbit, ticker) :
    """수익률"""
    balances = _upbit.get_balances()
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

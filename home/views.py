from asyncio.windows_events import NULL
from django.shortcuts import render, redirect

from home.models import *
from django.http import HttpResponseRedirect, JsonResponse

import pyupbit

from home import auto_trade_thread as att

import bcrypt

_upbit = NULL
auto_trade_thread = NULL

def login_html(request) :
    """
        login Page
    """
    return render(request, 'login.html')

def goHome(request) :
    """
        login Page
        login
    """
    result = True
    try :
        _user = User.objects.get(user_id=request.POST.get('user_id'));
        if not bcrypt.checkpw(request.POST.get('user_pw').encode('utf-8'), _user.user_pw.encode('utf-8')) :
            result = False
    except :
        result = False
    print("result = ", result)
    if result :
        """upbit 로그인"""
        _access_key = _user.access_key
        _secret_key = _user.secret_key

        global _upbit, auto_trade_thread
        status = Status.objects.get(id=1)
        _upbit = pyupbit.Upbit(_access_key, _secret_key)
        if auto_trade_thread == NULL :
            auto_trade_thread = att.Worker(_upbit, status.trade_method_id)
            auto_trade_thread.daemon = True
    
    context = {"result" : result}
    return JsonResponse(context)

def user_join_html(request) :
    """
        join Page
    """
    return render(request, 'join.html')

def checkId(request) :
    """
        join Page
        Ajax
        id overlap check
    """
    result = False
    try :
        User.objects.get(user_id=request.POST.get('user_id'))
    except :
        result = True
    context = {"result" : result}
    return JsonResponse(context)

def joinFinish(request) :
    """
        join Page
        insert into home_user
    """
    _user = User();
    _user.user_id = request.POST.get('user_id')
    _user_pw = bcrypt.hashpw(password=request.POST.get('user_pw').encode('utf-8'), salt=bcrypt.gensalt())
    _user.user_pw = _user_pw[2:-1]
    _user.save();
    return redirect("/login/")

def logout(request) :
    """
        logout
    """
    global _upbit, auto_trade_thread
    _upbit = NULL
    auto_trade_thread = NULL
    return render(request, 'login.html')
    # return redirect('/login/')

def home_html(request) :
    """
        전체 계좌 조회 Page
    """
    global _upbit
    df = _upbit.get_balances_tickers()
    qs = [vals for vals in df.to_dict('records')]
    data = {'data':qs}
    return render(request, 'home.html', data)

def transHistory_html(request) :
    """
        거래 내역 Page
    """
    global _upbit
    markets = pyupbit.get_tickers(fiat="KRW");
    markets = [market[4:] for market in markets]
    markets.sort()
    orders = _upbit.get_order_list("KRW-BTC") if request.POST.get('nav_select_market') == None else att.upbit.get_order_list("KRW-"+request.POST.get('nav_select_market'))
    data = {'markets': markets, 'orders' : orders, 'select_market':request.POST.get('nav_select_market')}
    return render(request, 'transHistory.html', data)

def onoff_html(request) :
    """
        Auto Trade Page
    """
    global auto_trade_thread
    print("auto_trade_thread.isAlive() = ", auto_trade_thread.isAlive())
    status_chk = Status.objects.filter(id=1)
    trade_method = Trade_method.objects.all()
    data = {'chk':status_chk[0], 'trade_method':trade_method}
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
        auto_trade_thread = att.Worker(_upbit, status.trade_method_id)
        auto_trade_thread.daemon = True
        auto_trade_thread.start()
        print("auto_trade_thread.isAlive() = ", auto_trade_thread.isAlive())
    elif request.POST.get('chk') == "False" :
        status.status_chk = True
        auto_trade_thread.kill()
    status.save()
    context = {"result" : "success"}
    return JsonResponse(context)

def changeMethod(request) :
    """
        Auto Trade Page
        Ajax
        thread method change
    """
    status = Status.objects.get(id=1)
    status.trade_method_id = request.POST.get('id')
    status.trade_method = request.POST.get('name')
    status.save()
    context = {"result" : "success"}
    return JsonResponse(context)


""" 참고용 추후에 삭제 """
def insertFage(request) :
    return render(request, 'insertFage.html')

def insert(request) :
    homeMethod = Trade_method()
    homeMethod.method_name = request.POST['method_name']
    homeMethod.method_text = request.POST['method_text']
    homeMethod.save()
    return HttpResponseRedirect('/onoff/')

def dataDelete(request) :
    test = Test.objects.get(id=request.POST['id'])
    test.delete()
    return HttpResponseRedirect('/')
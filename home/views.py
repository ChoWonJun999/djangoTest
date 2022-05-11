from django.shortcuts import render

from home.models import *
from django.http import HttpResponseRedirect, JsonResponse

from home import auto_trade_thread as att

import pyupbit

auto_trade_thread = att.auto_trade_thread
upbit = att.upbit

_user_pk = 0

def login_html(request) :
    return render(request, 'login.html')

def goHome(request) :
    result = True
    try :
        _user = User.objects.get(user_id=request.POST.get('user_id'), user_pw=request.POST.get('user_pw'));
        global _user_pk
        _user_pk = _user.id
    except :
        result = False
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
        User.objects.get(user_id=request.POST.get('user_id'));
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
    _user.user_id = request.POST.get('user_id');
    _user.user_pw = request.POST.get('user_pw');
    _user.save();
    return render(request, 'login.html')

def logout(request) :
    global _user_pk
    _user_pk = 0
    return login_html(request)

def home_html(request) :
    """
        전체 계좌 조회 Page
    """
    global _user_pk
    if _user_pk == 0 : return render(request, 'login.html')

    df = upbit.get_balances_tickers()
    qs = [vals for vals in df.to_dict('records')]
    data = {'data':qs}
    return render(request, 'home.html', data)

def transHistory_html(request) :
    """
        거래 내역 Page
    """
    global _user_pk
    if _user_pk == 0 : return render(request, 'login.html')

    markets = pyupbit.get_tickers(fiat="KRW");
    markets = [market[4:] for market in markets]
    markets.sort()
    orders = upbit.get_order_list("KRW-BTC") if request.POST.get('nav_select_market') == None else att.upbit.get_order_list("KRW-"+request.POST.get('nav_select_market'))
    data = {'markets': markets, 'orders' : orders, 'select_market':request.POST.get('nav_select_market')}
    return render(request, 'transHistory.html', data)

def onoff_html(request) :
    """
        Auto Trade Page
    """
    global _user_pk
    if _user_pk == 0 : return render(request, 'login.html')

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
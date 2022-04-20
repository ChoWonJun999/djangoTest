from django.shortcuts import render
from requests import request
import numpy as np

from home.models import *
from django.http import HttpResponseRedirect, JsonResponse

import threading
import time
from home import AutoTradeModule

def home(request) :
    test = Test.objects.all().order_by('-id')
    data = {'test':test}
    return render(request, 'home.html', data)

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        AutoTradeModule.trade()

def onoff(request) :
    status_chk = Status.objects.filter(id=1)
    data = {'chk':status_chk[0]}
    return render(request, 'onoff.html', data)

def changeStatus(request) :
    # t = Worker()
    # t.daemon = True
    # t.start()
    status = Status.objects.get(id=1)
    if request.POST.get('chk') == "True" :
        status.status_chk = False
        # t.start()
    elif request.POST.get('chk') == "False" :
        status.status_chk = True
        # os.system("pause")
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
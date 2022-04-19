from django.shortcuts import render, HttpResponse
from requests import request

from home.models import Test
from django.http import HttpResponseRedirect

import threading
import time
from home import AutoTradeModule

def home(request) :
    # t = Worker()
    # t.daemon = True
    # t.start()
    test = Test.objects.all().order_by('-id')
    data = {'test':test}
    return render(request, 'home.html', data)

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        AutoTradeModule.trade()

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
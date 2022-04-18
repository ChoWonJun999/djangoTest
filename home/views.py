from django.shortcuts import render, HttpResponse
from requests import request

import threading
import time
from home import AutoTradeModule

def home(request) :
    # t = Worker()
    # t.daemon = True
    # t.start()
    # return HttpResponse(HTMLTeplate())
    return render(request, 'home.html')

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        AutoTradeModule.trade()

def HTMLTeplate(tag = None) :
    return f'''
    <html>
    <body>
        <h1><a href="/">Home</a></h1>
        <ul>
        </ul>
        <ul>
            <li>
                {tag}
            </li>
            <li>
                <a href="/create/">create</a>
            </li>
        </ul>
    </body>
    </html>
    '''

def create(request) :
    return HttpResponse(HTMLTeplate())
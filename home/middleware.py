from home.models import User
from django.shortcuts import render, redirect
_user = ""
_chk = 0
def StatisticsMiddleware(get_response):
    def middleware(request):
        global _user, _chk
        if request.path_info == "/goHome/" :
            _user = User.objects.filter(user_id=request.POST.get('user_id'), user_pw=request.POST.get('user_pw'));
            _chk = 1
        elif request.path_info == "/logout/" :
            _user = ""
            _chk = 0
        if request.path_info != "/login/" and _user == "" :
            return redirect('/login/')
        elif request.path_info == "/login/" and _user != "" :
            return redirect('/')
        response = get_response(request)
        response.set_cookie("chk", _chk, max_age=None)
        return response
    return middleware
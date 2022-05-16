from home.models import User
from django.shortcuts import redirect
import bcrypt
_user = ""
def StatisticsMiddleware(get_response):
    def middleware(request):
        global _user
        if request.path_info == "/goHome/" :
            try :
                _user = User.objects.get(user_id=request.POST.get('user_id'));
                if not bcrypt.checkpw(request.POST.get('user_pw').encode('utf-8'), _user.user_pw[2:-1].encode('utf-8')) :
                    _user = ""
                    response = get_response(request)
                    return response
            except :
                response = get_response(request)
                return response
        elif request.path_info == "/logout/" :
            _user = ""
        
        if request.path_info != "/join/" and request.path_info != "/checkId/" and request.path_info != "/joinFinish/" and request.path_info != "/checkApiKey/" :
            if request.path_info != "/login/" and _user == "" :
                return redirect('/login/')
            elif request.path_info == "/login/" and _user != "" :
                return redirect('/')
        
        response = get_response(request)
        return response
    return middleware
from home.models import User
from django.shortcuts import redirect
_user = ""
def StatisticsMiddleware(get_response):
    def middleware(request):
        global _user
        if request.path_info == "/goHome/" :
            try :
                _user = User.objects.get(user_id=request.POST.get('user_id'), user_pw=request.POST.get('user_pw'));
            except :
                response = get_response(request)
                return response
        elif request.path_info == "/logout/" :
            _user = ""
        
        if request.path_info != "/login/" and _user == "" :
            return redirect('/login/')
        elif request.path_info == "/login/" and _user != "" :
            return redirect('/')
        
        response = get_response(request)
        return response
    return middleware
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib

# Create your views here.

def reg_view(request):
    if request.method == "GET":
        return render(request,"user/register.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            return HttpResponse("两次密码不一致！请重新输入！")
        m = hashlib.md5()
        m.update(password1.encode())
        password_m = m.hexdigest()
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse("该用户名已被注册！")
        try:
            user = User.objects.create(username = username,password = password_m)
        except Exception as e:
            print("用户重复创建！{}".format(e))
            return HttpResponse("该用户名已被注册！")
        request.session["uname"] = username
        request.session['uid'] = user.id
        return HttpResponseRedirect("/index/index")


def login_view(request):
    if request.method == "GET":
        if request.session.get("uname") and request.session.get("uid"):
            return HttpResponseRedirect("/index/index")
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            request.session['uname'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect("index/index")
        return render(request,"user/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            s_username = User.objects.get(username = username)
        except Exception as e:
            print("未查询到此用户,{}".format(e))
            return HttpResponse("用户名或密码不正确")
        m = hashlib.md5()
        m.update(password.encode())
        if m.hexdigest() != s_username.password:
            return HttpResponse("用户名或密码不正确")
        request.session["uname"] = username
        request.session['uid'] = s_username.id
        result = HttpResponseRedirect("/index/index")
        if 'remember' in request.POST:
            result.set_cookie("username",username,3600*24*3)
            result.set_cookie("uid",s_username.id,3600*24*3)
        return result

def logout_view(request):
    if "uname" in request.session:
        del request.session["uname"]
    if "uid" in request.session:
        del request.session["uid"]

    resp = HttpResponseRedirect("/index/index")
    if "username" in request.COOKIES:
       resp.delete_cookie("username")
    if "uid" in request.COOKIES:
        resp.delete_cookie("uid")
    return resp
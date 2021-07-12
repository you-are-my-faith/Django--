from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Notes

# Create your views here.
def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'uname' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_uid or not c_username:
                return HttpResponseRedirect("/user/login")
            else:
                request.session['uname'] = c_username
                request.session['uid'] = c_uid
        return fn(request,*args,**kwargs)
    return wrap

def list_view(request):
    notes_list = Notes.objects.all()
    return render(request,"notes/list_note.html",locals())

@check_login
def add_view(request):
    if request.method == "GET":
        return render(request,"notes/add_note.html")
    elif request.method == "POST":
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Notes.objects.create(user_id = uid,title = title,content = content)
        return HttpResponse("添加笔记成功")
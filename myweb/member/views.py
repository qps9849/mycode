from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as dlogin,logout as dlogout
from member.models import UserForm,LoginForm
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if not request.user.is_authenticated:
        data={"username": request.user,
              "is_authenticated": request.user.is_authenticated}
    else:
        data={"last_login": request.user.last_login,
              "username":request.user.username,
              "password":request.user.password,
              "is_authenticated":request.user.is_authenticated}
    return render(request, "member/index.html",{"data":data})

def join(request):
    if request.method == "POST":
        form=UserForm(request.POST)
        if form.is_valid():
            new_user=User.objects.create_user(**form.cleaned_data)
            dlogin(request,new_user)
            return redirect("/member")
        else:
            return render(request,"member/index.html",
                          {"msg":"회원가입 실패...다시 시도해 보세요."})
    else:
        form=UserForm()
        return render(request,"member/join.html",{"form":form})

@csrf_exempt
def login_check(request):
    if request.method=="POST":
        name=request.POST["username"]
        pwd=request.POST["password"]
        user=authenticate(username=name, password=pwd)
        if user is not None:
            dlogin(request,user)
            request.session["userid"]=name
            return redirect("/member/")
        else:
            return render(request, "member/index.html",
                          {"msg":"로그인 실패... 다시 시도해 보세요."})
    else:
        form=LoginForm()
        return  render(request,"member/login.html",{"form":form})

def logout(request):
    dlogout(request)
    return redirect("/member")

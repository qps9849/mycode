from guestbook.models import Guestbook
import math
import os
from django.shortcuts import render,redirect
from django.db.models import Q
from django.utils.http import urlquote

def list(request):
    try:
        searchkey=request.POST["searchkey"]
    except:
        searchkey="name"

    try:
        search= request.POST["search"]
    except:
        search=""

    if searchkey == "name_content":
        gbList=Guestbook.objects.filter(\
            Q(name__contains=search)|Q(content__contains=search)).order_by("-idx")
    elif searchkey=="name":
        gbList = Guestbook.objects.filter(name__contains=search).order_by("-idx")
    elif searchkey=="content":
        gbList = Guestbook.objects.filter(content__contains=search).order_by("-idx")

    try:
        msg=request.GET["msg"]
    except:
        msg=""

    return render(request,"guestbook/list.html",{"gbList":gbList,"gbCount": len(gbList),
                                                 "searchkey":searchkey,"search":search,"msg":msg})

def write(request):
    return render(request,"guestbook/write.html")

def insert(request):
    row=Guestbook(name=request.POST["name"],email=request.POST["email"],\
            passwd=request.POST["passwd"],content=request.POST["content"])
    row.save()
    print(row)
    return redirect("/guestbook")

def passwd_check(request):
    id=request.POST["idx"]
    pwd=request.POST["passwd"]
    row=Guestbook.objects.get(idx=id)
    if row.passwd==pwd:
        return render(request, "guestbook/edit.html",{"row":row})
    else:
        return redirect("/guestbook/?msg=error")

def update(request):
    id=request.POST['idx']
    row=Guestbook(idx=id,name=request.POST["name"],email=request.POST["email"],passwd=request.POST["passwd"],content=request.POST["content"])

    row.save()
    return redirect("/guestbook")

def delete(request):
    id=request.POST["idx"]
    Guestbook.objects.get(idx=id).delete()
    return redirect("/guestbook")

from django.shortcuts import redirect,render
from memo.models import Memo

def home(request):
    memoList=Memo.objects.order_by("idx")
    return render(request, 'memo/list.html', \
                  {'memoList':memoList, 'memoCount':len(memoList)})

def insert_memo(request):
    memo=Memo(writer=request.POST['writer'], memo=request.POST['memo'])
    memo.save()
    return redirect('/memo')

def detail(request):
    id=request.GET['idx']
    row=Memo.objects.get(idx=id)
    return render(request, 'memo/detail.html',{'row':row})

def update_memo(request):
    id = request.POST['idx']
    memo=Memo(idx=id, writer=request.POST['writer'],\
              memo=request.POST['memo'])
    memo.save()
    return redirect("/memo")

def delete_memo(request):
    id=request.POST['idx']
    Memo.objects.get(idx=id).delete()
    return redirect("/memo")

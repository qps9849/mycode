from django.shortcuts import render,redirect
from address.models import Address

def home(request):
    items = Address.objects.order_by("name")
    return render(request, 'address/list.html', \
                  {'items': items,'address_count':len(items)})

def write(request):
    return render(request, "address/write.html")

def insert(request):
    addr=Address(name=request.POST['name'], tel=request.POST['tel'],\
                 email=request.POST['email'], address=request.POST['address'])
    addr.save()
    return redirect("/address")

def detail(request):
    id=request.GET['idx']
    addr=Address.objects.get(idx=id)
    return render(request, 'address/detail.html',{'addr':addr})

def update(request):
    id=request.POST['idx']
    addr=Address(idx=id,name=request.POST['name'],tel=request.POST['tel'],\
                 email=request.POST['email'],address=request.POST['address'])
    addr.save()
    return redirect('/address')

def delete(request):
    id=request.POST['idx']
    Address.objects.get(idx=id).delete()
    return redirect("/address")
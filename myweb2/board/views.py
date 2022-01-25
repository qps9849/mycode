import math
import os
from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from board.models import Board, Comment
from django.utils.http import urlquote
UPLOAD_DIR="c:/upload/"

def list(request):
    try:
        search_option=request.POST["search_option"]
    except:
        search_option="writer"

    try:
        search=request.POST["search"]
    except:
        search=""

    boardCount=Board.objects.count()

    try:
        start=int(request.GET['start'])
    except:
        start=0

    page_size=10
    page_list_size=10
    end=start+page_size
    total_page=math.ceil(boardCount/page_size)
    current_page=math.ceil((start+1)/page_size)
    start_page= math.floor((current_page-1)/page_list_size)*page_list_size+1
    end_page=start_page+page_list_size-1
    if total_page < end_page:
        end_page=start_page+page_list_size-1
    if start_page >= page_list_size:
        prev_list=(start_page-2)*page_size
    else:
        prev_list=0
    if total_page > end_page:
        next_list = end_page * page_size
    else:
        next_list=0

    if search_option == "all":
        boardList=Board.objects.filter(Q(writer__contains=search)|
                                       Q(title__contains=search)|
                                       Q(content__contains=search)).order_by("idx")[start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(writer__contains=search).order_by("-idx")[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(title__contains=search).order_by("-idx")[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(content__contains=search).order_by("-idx")[start:end]

    print("start_page:", start_page)
    print("end_page:", end_page)
    print("page_list_size:", page_list_size)
    print("total_page:", total_page)
    print("prev_list:", prev_list)
    print("next_list:", next_list)
    links=[]
    for i in range(start_page,end_page+1):
        page=(i-1)*page_size
        links.append("<a href='?start="+str(page)+"'>"+str(i)+"</a>")
    print("links:",links)
    return render(request, "list.html",
                  {"boardList": boardList, "boardCount": len(boardList),
                   "search_option": search_option,"search": search,
                   "range": range(start_page- 1, end_page), "start_page": start_page,
                   "end_page": end_page,"page_list_size": page_list_size,
                   "total_page": total_page, "prev_list": prev_list,
                   "next_list": next_list, "links": links})

def write(request):
    return render(request,"write.html")

def insert(request):
    fname=""
    fsize=0
    if "file" in request.FILES:
        file=request.FILES["file"]
        fname=file._name
        with open("%s%s"%(UPLOAD_DIR,fname),"wb")as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        fsize=os.path.getsize(UPLOAD_DIR+fname)
    row=Board(writer=request.POST["writer"],title=request.POST["title"],
              content=request.POST["content"],filename=fname,
              filesize=fsize)
    row.save()
    print(row)
    return redirect("/")

def detail(request):
    id = request.GET["idx"]
    row = Board.objects.get(idx=id)
    row.hit_up()
    row.save()
    commentList = Comment.objects.filter(board_idx=id).order_by("idx")
    print("filesize:", row.filesize)
    filesize = "%.2f" % (row.filesize / 1024)
    return render(request, "detail.html", {"row": row,
                                           "filesize": filesize,
                                           "commentList": commentList})

def update(request):
    id = request.POST['idx']
    row_src = Board.objects.get(idx=id)
    fname = row_src.filename
    fsize = row_src.filesize
    hit=row_src.hit
    down=row_src.down
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file._name
        with open("%s%s" % (UPLOAD_DIR, fname), "wb") as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        fsize = os.path.getsize(UPLOAD_DIR + fname)
    row_new = Board(idx=id, writer=request.POST["writer"],
                    title=request.POST["title"], content=request.POST["content"],
                    filename=fname, filesize=fsize, hit=hit, down=down)
    row_new.save()
    return redirect("/")

def delete(request):
    id = request.POST["idx"]
    Board.objects.get(idx=id).delete()
    return redirect("/")

def download(request):
    id = request.GET['idx']
    row = Board.objects.get(idx=id)
    path = UPLOAD_DIR + row.filename
    print("path:", path)
    filename = os.path.basename(path)
    filename = urlquote(filename)

    print("pfilename:", os.path.basename(path))
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{0}".format(filename)
        row.down_up()
        row.save()
        return response

def reply_insert(request):
    id = request.POST["idx"]
    row = Comment(board_idx=id, writer=request.POST["writer"],
                  content=request.POST["content"])
    row.save()

    return HttpResponseRedirect("detail?idx=" + id)

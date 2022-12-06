from django.shortcuts import render, redirect
from .models import Memo
from login.decorators import *


def memo(request):
    q = request.POST.get('q', False)
    if q:
        memos = Memo.objects.filter(title__icontains=q).order_by("-id")
    else:
        memos = Memo.objects.all().order_by("-id")
    return render(request, 'memo/memo.html', {"memos":memos})


@login_message_required
def create_memo(request):
    content = request.POST['memo']  
    new_memo = Memo(title=content)
    new_memo.save()
    return redirect('/memo/list')

@login_message_required
def delete_memo(request, pk):
    memo = Memo.objects.get(id=pk)
    memo.delete()
    return redirect('/memo/list')

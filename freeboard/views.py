import urllib
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Freeboard, Comment
from django.contrib import messages
from django.db.models import Q
from login.decorators import *
from .forms import FreeboardWriteForm
import os
from django.http import HttpResponse, Http404
import mimetypes
import json
from django.core.serializers.json import DjangoJSONEncoder


class AllListView(ListView):
    model = Freeboard
    paginate_by = 10
    template_name = 'freeboard/freeboard_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'freeboard_list'        #DEFAULT : <model_name>_list

    # Django Paginator 하단부의 페이지 숫자 범위를 커스텀
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        freeboard_fixed = Freeboard.objects.filter(top_fixed=True).order_by('-registered_date')
        context['freeboard_fixed'] = freeboard_fixed

        if len(search_keyword) > 1 :
            context['q'] = search_keyword
        context['type'] = search_type

        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1        
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range        
        end_index = start_index + page_numbers_range
        
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        freeboard_list = Freeboard.objects.order_by('-id') 
        
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__username__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_freeboard_list = freeboard_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_freeboard_list = freeboard_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_freeboard_list = freeboard_list.filter(writer__user_id__icontains=search_keyword)

                return search_freeboard_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return freeboard_list


# 카테고리 자유만 보기
class FreeListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        freeboard_list = Freeboard.objects.filter(category='자유').order_by('-id')
        
        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_freeboard_list = freeboard_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_freeboard_list = freeboard_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_freeboard_list = freeboard_list.filter(writer__user_id__icontains=search_keyword)

                return search_freeboard_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return freeboard_list


# 카테고리 GHSH만 보기
class GshsListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        freeboard_list = Freeboard.objects.filter(category='GSHS').order_by('-id')

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_freeboard_list = freeboard_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_freeboard_list = freeboard_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_freeboard_list = freeboard_list.filter(writer__user_id__icontains=search_keyword)
        
                return search_freeboard_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return freeboard_list


# 카테고리 LINUX만 보기
class LinuxListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        freeboard_list = Freeboard.objects.filter(category='LINUX').order_by('-id')

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_freeboard_list = freeboard_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_freeboard_list = freeboard_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_freeboard_list = freeboard_list.filter(writer__user_id__icontains=search_keyword)
                    
                return search_freeboard_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return freeboard_list


# 카테고리 WINDOW만 보기
class WindowListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        freeboard_list = Freeboard.objects.filter(category='WINDOW').order_by('-id')

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_freeboard_list = freeboard_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_freeboard_list = freeboard_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_freeboard_list = freeboard_list.filter(writer__user_id__icontains=search_keyword)
                    
                return search_freeboard_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return freeboard_list


# 카테고리 WINDOW만 보기
class CodeListView(AllListView):
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        freeboard_list = Freeboard.objects.filter(category='CODE').order_by('-id')

        if search_keyword :
            if len(search_keyword) > 1 :
                if search_type == 'all':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_freeboard_list = freeboard_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
                elif search_type == 'title':
                    search_freeboard_list = freeboard_list.filter(title__icontains=search_keyword)    
                elif search_type == 'content':
                    search_freeboard_list = freeboard_list.filter(content__icontains=search_keyword)    
                elif search_type == 'writer':
                    search_freeboard_list = freeboard_list.filter(writer__user_id__icontains=search_keyword)
                    
                return search_freeboard_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return freeboard_list


def freeboard_detail_view(request, pk):
    freeboard = get_object_or_404(Freeboard, pk=pk)   
    session_cookie = request.session.get('username', False)
    cookie_name = F'freeboard_hits:{session_cookie}'
    comment = Comment.objects.filter(post=pk).order_by('created')
    comment_count = comment.count()
    comment_count = comment.exclude(deleted=True).count()
    reply = comment.exclude(reply='0')

    if request.user == freeboard.writer:
        freeboard_auth = True
    else:
        freeboard_auth = False    

    context = {
        'freeboard': freeboard,
        'freeboard_auth': freeboard_auth,
        'comments': comment,
        'comment_count': comment_count,
        'replys': reply,
    }

    response = render(request, 'freeboard/freeboard_detail.html', context)
   
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')

        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            freeboard.hits += 1
            freeboard.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        freeboard.hits += 1
        freeboard.save()
        return response

    return render(request, 'freeboard/freeboard_detail.html', context)


@login_message_required
def freeboard_write_view(request):
    if request.method == "POST":
        form = FreeboardWriteForm(request.POST, request.FILES)
        user = request.user.username
        username = User.objects.get(username = user)
        
        if form.is_valid():
            freeboard = form.save(commit = False)
            freeboard.writer = username
            if request.FILES:
                if 'upload_files' in request.FILES.keys():
                    freeboard.filename = request.FILES['upload_files'].name                    
            freeboard.save()
            return redirect('freeboard:all_list')
    else:
        form = FreeboardWriteForm()

    return render(request, "freeboard/freeboard_write.html", {'form': form})


@login_message_required
def freeboard_edit_view(request, pk):
    freeboard = Freeboard.objects.get(id=pk)
    
    if request.method == "POST":
        if freeboard.writer == request.user: #or request.user.level == '0'
            file_change_check = request.POST.get('fileChange', False)
            file_check = request.POST.get('upload_files-clear', False)

            if file_check or file_change_check:
                os.remove(os.path.join(settings.MEDIA_ROOT, freeboard.upload_files.path))

            form = FreeboardWriteForm(request.POST, request.FILES, instance=freeboard)
            if form.is_valid():
                freeboard = form.save(commit = False)
                if request.FILES:
                    if 'upload_files' in request.FILES.keys():
                        freeboard.filename = request.FILES['upload_files'].name
                freeboard.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/freeboard/'+str(pk))
    else:
        freeboard = Freeboard.objects.get(id=pk)
        if freeboard.writer == request.user: # or request.user.level == '0'
            form = FreeboardWriteForm(instance=freeboard)
            context = {
                'form': form,
                'edit': '수정하기',
            }
            if freeboard.filename and freeboard.upload_files:
                context['filename'] = freeboard.filename
                context['file_url'] = freeboard.upload_files.url
                
            return render(request, "freeboard/freeboard_write.html", context)
        else:
            messages.error(request, "본인 게시글이 아닙니다.")
            return redirect('/freeboard/'+str(pk))


@login_message_required
def freeboard_delete_view(request, pk):
    freeboard = Freeboard.objects.get(id=pk)
    if freeboard.writer == request.user: # or request.user.level == '0'
        freeboard.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('/freeboard/')
    else:
        messages.error(request, "본인 게시글이 아닙니다.")
        return redirect('/freeboard/'+str(pk))


@login_message_required
def freeboard_download_view(request, pk):
    freeboard = get_object_or_404(Freeboard, pk=pk)
    url = freeboard.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(freeboard.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404


@login_message_required
def comment_write_view(request, pk):
    post = get_object_or_404(Freeboard, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(post=post, content=content, writer=request.user)
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'writer': writer,
            'content': content,
            'created': '방금 전',
            'comment_id': comment.id
        }
        if request.user == post.writer:
            data['self_comment'] = '(글쓴이)'
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


@login_message_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Freeboard, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)

    if request.user == target_comment.writer:
        target_comment.deleted = True
        target_comment.save()
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'comment_id': comment_id,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")

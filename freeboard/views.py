import urllib
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Freeboard
from django.contrib import messages
from django.db.models import Q
from login.decorators import *
from .forms import FreeboardWriteForm
import os
from django.http import HttpResponse, Http404
import mimetypes


class FreeboardListView(ListView):
    model = Freeboard
    paginate_by = 5
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


@login_message_required
def freeboard_detail_view(request, pk):
    freeboard = get_object_or_404(Freeboard, pk=pk)    
    if request.user == freeboard.writer:
        freeboard_auth = True
    else:
        freeboard_auth = False
    session_cookie = request.session['username']
    cookie_name = F'freeboard_hits:{session_cookie}'

    context = {
        'freeboard': freeboard,
        'freeboard_auth': freeboard_auth,
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
            return redirect('freeboard:freeboard_list')
    else:
        form = FreeboardWriteForm()

    return render(request, "freeboard/freeboard_write.html", {'form': form})


@login_message_required
def freeboard_edit_view(request, pk):
    freeboard = Freeboard.objects.get(id=pk)
    
    if request.method == "POST":
        if freeboard.writer == request.user: #or request.user.level == '0'
            form = FreeboardWriteForm(request.POST, instance=freeboard)
            if form.is_valid():
                freeboard = form.save(commit = False)
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
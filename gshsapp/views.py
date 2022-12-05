from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView
from .models import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.template.loader import render_to_string
import datetime
import xlwt
from login.decorators import *
from django.utils.decorators import method_decorator


def home(request):
    return render(request, 'gshsapp/home.html')
    
def InfogigiList(request, gigigubun):    
    context={}
    query = request.GET.get('q','') 

    if gigigubun == 'all':            
        infogigis = Gigiinfo.objects.all().exclude(user__is_active =False).filter(jaego=False, notuse=False).order_by('date')
    elif gigigubun == 'notebook' or gigigubun == 'desktop':            
        infogigis = Gigiinfo.objects.all().exclude(user__is_active =False).filter(buyproduct__gubun__gubun=gigigubun, jaego=False, notuse=False).order_by('date')
    elif gigigubun == 'jaego':
        infogigis = Gigiinfo.objects.all().filter(jaego=True, notuse=False).order_by('date')
    elif gigigubun == 'notuse':    
        infogigis = Gigiinfo.objects.all().filter(jaego=False, notuse=True).order_by('date')
    else:
        infogigis = Gigiinfo.objects.all().filter(buyproduct__gubun__gubun=gigigubun, jaego=False, notuse=False).order_by('date')
           
        
    gigis = infogigis.filter(Q(user__name__icontains=query) | Q(buyproduct__model__icontains=query) | Q(location__hosil__icontains=query) | Q(ip__icontains=query))
    context['gigigubun'] = gigigubun 
    context['q'] = query
    page = request.GET.get('page', '1')  # 페이지    
    paginator = Paginator(gigis, 10)  # 페이지당 10개씩 보여주기    
    page_obj = paginator.get_page(page)    
    context ['page_obj'] = page_obj
    context ['query'] = query
    
    return render(request, 'gshsapp/infogigi.html', context)


@method_decorator(login_message_required, name='dispatch')
class InfogigiCV(CreateView):
    model = Gigiinfo
    template_name = 'gshsapp/create.html'
    form_class = GigiinfoForm 

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['gigi_gubun'] = self.kwargs['gigigubun']
        return kwargs
   
    def get_success_url(self):        
        return reverse('gshsapp:gigi_gubun', kwargs={'gigigubun': self.object.buyproduct.gubun.gubun})
   

@login_message_required
def InfogigiDel(request, pk):
    gigiinfo= get_object_or_404(Gigiinfo, pk=pk)
    
    repairs = gigiinfo.repair.all()
    if repairs:
        for i in repairs:
            i.delete()

    changes = gigiinfo.replacement.all()
    if changes:
        for i in changes:
            i.delete()    
    
    gigiinfo.delete()
    
    return JsonResponse({'data':True}, status=200)

@method_decorator(login_message_required, name='dispatch')
class InfogigiUV(UpdateView):
    model = Gigiinfo
    template_name = 'gshsapp/snipet/infogigi_update.html'
    form_class = GigiinfoForm

    def get_success_url(self):
        return reverse('gshsapp:gigi_gubun', kwargs={'gigigubun': self.object.buyproduct.gubun.gubun})
    
@login_message_required
def InfogigiChange(request, pk):
    gigiinfo2 = get_object_or_404(Gigiinfo, pk=pk)    
    ImageFormSet = modelformset_factory(Change_Photo, form=Change_PhotoForm, extra=3)
    
    if request.method == 'POST':
        changeform = InfogigiChangeForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Change_Photo.objects.none())
        
        if changeform.is_valid() and formset.is_valid():
            change = changeform.save()      
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Change_Photo(replacement=change, image=image) 
                    photo.save()   
            
            return redirect('gshsapp:gigi_gubun', gigiinfo2.buyproduct.gubun.gubun)
    else:
        changeform = InfogigiChangeForm(initial={'gigiinfo':gigiinfo2})
        formset = ImageFormSet(queryset=Change_Photo.objects.none())
        
    return render(request, 'gshsapp/snipet/infogigi_gigichange.html', {'form': changeform, 'formset': formset})


@login_message_required
def InfogigiSuri(request, pk):
    gigiinfo2 = get_object_or_404(Gigiinfo, pk=pk)
   
    if request.method == 'POST':
        suriform = InfogigiSuriForm(request.POST)
       
        if suriform.is_valid():
            suri = suriform.save()
            
            for img in request.FILES.getlist('imgs'):
                repair_Photo = Repair_Photo()
                repair_Photo.repair = suri
                repair_Photo.image = img
                repair_Photo.save()

            return redirect('gshsapp:gigi_gubun', gigiinfo2.buyproduct.gubun.gubun)
    else:
        form = InfogigiSuriForm(initial={'gigiinfo':gigiinfo2}) 
       
    return render(request, 'gshsapp/snipet/infogigi_gigisuri.html', {'form': form})

# 부서전체 로딩 및 연도 선택시 뷰
def InfogigiBuseo(request, buseogubun):
    gubun = request.GET.get('gubun',False)    
    if gubun:
        data = {}
        data['gubun'] = gubun
        changeyear = request.GET.get('buseoyear','')
        buseogubun = request.GET.get('buseogubun','')        

        a_date = changeyear +"-3-1"
        start_date = datetime.datetime.strptime(a_date, '%Y-%m-%d').date()
        end_date = start_date+ datetime.timedelta(days=364)  
        
        
        if gubun == 'change':
            changes = Replacement.objects.filter(gigiinfo__location__hosil=buseogubun, date__range=[start_date, end_date]).annotate(changeTotal = F('count') *  F('cost'))
            changeTotalCost = changes.aggregate(Sum('changeTotal'))
            data['html_buseo'] = render_to_string('gshsapp/snipet/buseo_change_list.html', {"changeyear":changeyear, "changes":changes, "changeTotalCost":changeTotalCost})
        else:
            repairs = Repair.objects.filter(gigiinfo__location__hosil=buseogubun, date__range=[start_date, end_date])
            repairTotalCost = repairs.aggregate(Sum('cost'))
            data['html_buseo'] = render_to_string('gshsapp/snipet/buseo_repair_list.html', {"changeyear":changeyear, "repairs":repairs, "repairTotalCost":repairTotalCost})
    
        return JsonResponse(data)
    else:
        buseos = Location.objects.filter(locationgubun='부서')
        gitas = Location.objects.exclude(locationgubun='부서')
        buseo_name = Location.objects.get(hosil=buseogubun)
        building = buseo_name.building

        a_date = str(datetime.datetime.today().year) +"-3-1"
        start_date = datetime.datetime.strptime(a_date, '%Y-%m-%d').date()
        end_date = start_date+ datetime.timedelta(days=364)  
        
        repairs = Repair.objects.filter(gigiinfo__location__hosil=buseogubun, date__range=[start_date, end_date])
        repairTotalCost = repairs.aggregate(Sum('cost'))
        
        changes = Replacement.objects.filter(gigiinfo__location__hosil=buseogubun, date__range=[start_date, end_date]).annotate(changeTotal = F('count') *  F('cost'))
        changeTotalCost = changes.aggregate(Sum('changeTotal'))

        members = buseo_name.gigiinfo.exclude(user__is_active =False).filter(jaego=False, notuse=False)    

        return render(request, 'gshsapp/buseo.html', {'buseos':buseos,'building':building, 'gitas':gitas, 'members':members, 'changes':changes,'repairs':repairs, 'buseogubun':buseogubun, 'repairTotalCost':repairTotalCost, 'changeTotalCost':changeTotalCost})

# 부서 부원 및 기기 ajax
@login_message_required
def InfogigiBuseoUpdate(request, pk):
    data = {}
    gigiinfo = get_object_or_404(Gigiinfo, pk=pk)    
   
    if request.method == 'POST':
        form = GigiinfoForm(request.POST, instance=gigiinfo)        
        buseogubun = form.instance.location.hosil
        buseo_name = Location.objects.get(hosil=buseogubun)
        members = buseo_name.gigiinfo.filter(Q(user__is_active =True) | Q(jaego=False) & Q(notuse=False)) 
        
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True               
            
            if form.instance.user:   
                data['buwon'] = True              
                data['html_buseo'] = render_to_string('gshsapp/snipet/buseo_buwon_list.html', {'members':members, 'buseogubun':buseogubun})            
            else:
                print(form.instance.user)
                data['html_buseo'] = render_to_string('gshsapp/snipet/buseo_gigi_list.html', {'members':members, 'buseogubun':buseogubun})            
        else:
            data['form_is_valid'] = False
    else:
        form = GigiinfoForm(instance=gigiinfo) 
    
    context = {'form':form}
    data['html_form'] = render_to_string('gshsapp/snipet/buseo_buwon_form.html', context, request=request)
    return JsonResponse(data)

# 부서내 소모품교체 업데이트
@login_message_required
def buseoCRUpdate(request, pk):
    data = {}
    gubun =  request.GET.get('crgubun')
    gubun2 =  request.POST.get('crgubun')  

    if gubun == 'change' or gubun2 == 'change':
        change = Replacement.objects.get(pk=pk)     
        changePhotos = change.change_photo.all()
        changePhotoCount = changePhotos.count()

        if request.method == 'POST':
            changeform = BuseoChangeForm(request.POST, instance=change)
            
            for i in range(1, changePhotoCount + 1):
                changephotoid = request.POST.get('crPhoto-' + str(i), False)
                deleteid = request.POST.get('deletePhoto-' + str(i), False)            

                if deleteid:         
                    cdphoto = Change_Photo.objects.get(id=changephotoid)
                    cdphoto.delete()
                
                cimg = request.FILES.get('img-' + str(i), False)
                if cimg:
                    cphoto = Change_Photo.objects.get(id=changephotoid)                    
                    cphoto.image = cimg
                    cphoto.save()
                            
            if changeform.is_valid():
                changes = changeform.save() 
                imgs = request.FILES.getlist('imgs')
                
                if imgs:
                    for img in imgs:
                        changephoto = Change_Photo()
                        changephoto.replacement = change
                        changephoto.image = img
                        changephoto.save()

                data['html_buseo'] = render_to_string('gshsapp/snipet/buseo_change_update_list.html', {'gigi': changes})
        else:
            changeform = BuseoChangeForm(instance=change)
            data['html_form'] = render_to_string('gshsapp/snipet/buseo_change_updateform.html', {'form': changeform, 'pk':pk, 'changePhotos':changePhotos}, request=request)
    
    else:
        repair = Repair.objects.get(pk=pk)     
        repairPhotos = repair.repair_photo.all()
        repairPhotoCount = repairPhotos.count()

        if request.method == 'POST':
            repairform = InfogigiSuriForm(request.POST, instance=repair)
            
            for i in range(1, repairPhotoCount + 1):
                repairphotoid = request.POST.get('crPhoto-' + str(i), False)
                deleteid = request.POST.get('deletePhoto-' + str(i), False)            

                if deleteid:         
                    rdphoto = Repair_Photo.objects.get(id=repairphotoid)
                    rdphoto.delete()
                
                rimg = request.FILES.get('img-' + str(i), False)
                if rimg:
                    rphoto = Repair_Photo.objects.get(id=repairphotoid)                    
                    rphoto.image = rimg
                    rphoto.save()
                            
            if repairform.is_valid():
                repairs = repairform.save() 
                imgs = request.FILES.getlist('imgs')
                
                if imgs:
                    for img in imgs:
                        repairphoto = Repair_Photo()
                        repairphoto.repair = repair
                        repairphoto.image = img
                        repairphoto.save()

                data['html_buseo'] = render_to_string('gshsapp/snipet/buseo_repair_update_list.html', {'gigi': repairs})
        else:
            repairform = InfogigiSuriForm(instance=repair)
            data['html_form'] = render_to_string('gshsapp/snipet/buseo_repair_updateform.html', {'form': repairform, 'pk':pk, 'repairPhotos':repairPhotos}, request=request)
    
    return JsonResponse(data)

# 교체 수리 삭제
@login_message_required
def buseoCRUdelete(request, pk):
    crgubun = request.GET.get('crgubun')
    if crgubun == 'change':
        changes = Replacement.objects.get(id=pk)
        changes.delete()
    elif crgubun == 'repair':
        repairs = Repair.objects.get(id=pk)
        repairs.delete()  

    return JsonResponse({'data':True}, status=200)    


# 엑셀 보내기
@login_message_required
def excelExport(request, gubun):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename=' + gubun +'.xls' 
    wb = xlwt.Workbook(encoding='ansi') #encoding은 ansi로 해준다.
    ws = wb.add_sheet(gubun) #시트 추가
    
    row_num = 0
    col_names = ['구매일', '성명', '건물', '부서(호실)', '제조사', '모델명', 'IP', '비고']
    pcol_names = ['구매일', '건물', '부서(호실)', '제조사', '모델명', 'IP', '색상','비고']
    
    if gubun == 'printer' or gubun == 'tv' or gubun == 'project':
        colNames = pcol_names
    else:
        colNames = col_names
    #열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(colNames):
        ws.write(row_num, idx, col_name)        
    
    #데이터 베이스에서 유저 정보를 불러온다
    if gubun == 'notebook' or gubun == 'desktop': 
        infogigis = Gigiinfo.objects.exclude(user__is_active =False).filter(buyproduct__gubun__gubun=gubun, jaego=False, notuse=False)\
            .order_by('date').values_list('date','user__name','location__building','location__hosil','buyproduct__company', 'buyproduct__model', 'ip','bigo')
    else:
        infogigis = Gigiinfo.objects.exclude(user__is_active =False).filter(buyproduct__gubun__gubun=gubun, jaego=False, notuse=False)\
            .order_by('date').values_list('date','location__building','location__hosil','buyproduct__company', 'buyproduct__model', 'ip','color', 'bigo')
    
    #유저정보를 한줄씩 작성한다.
    for row in infogigis:
        row_num +=1
        for col_num, attr in enumerate(row):      
            if isinstance(attr, datetime.date):
                date_time = attr.strftime('%Y-%m-%d')
                ws.write(row_num, col_num, date_time)
            else:
                ws.write(row_num, col_num, attr)
            
    wb.save(response)
    return response
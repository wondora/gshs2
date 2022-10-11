from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from .models import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse
from django.forms import modelformset_factory


def home(request):
    return render(request, 'gshsapp/home.html')

class InfogigiLV(ListView):
    model = Gigiinfo
    paginate_by = 10 # 한 페이지에 보여줄 오브젝트의 갯수
    template_name = 'gshsapp/infogigi.html'
    # context_object_name = 'gigis'
    # queryset = Gigiinfo.objects.filter(jaego=False, notuse=False).order_by('buyproduct__buydate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gigigubun'] = self.kwargs['gigigubun']
        context['gigis'] = Gigiinfo.objects.filter(buyproduct__gubun__gubun=self.kwargs['gigigubun'], jaego=False, notuse=False).order_by('buyproduct__buydate')
        return context


class InfogigiUV(UpdateView):
    model = Gigiinfo
    template_name = 'gshsapp/update.html'
    form_class = GigiinfoForm
    context_object_name = 'gigis'
    success_url = '/' 
    
    def get_object(self): 
        review = get_object_or_404(Gigiinfo, pk=self.kwargs['pk'])         
        return review

    def get_success_url(self):
        return reverse('gshsapp:gigi_gubun', kwargs={'gigigubun': self.object.buyproduct.gubun.gubun})
    

def InfogigiChange(request, pk):
    gigiinfo2 = Gigiinfo.objects.get(pk=pk)
    ImageFormSet = modelformset_factory(Change_Photo, form=Change_PhotoForm, extra=3)

    if request.method == 'POST':
        changeform = InfogigiChangeForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Change_Photo.objects.none())

        if changeform.is_valid() and formset.is_valid():
            change = changeform.save()      
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    # print(form)
                    # print(form['image'])
                    photo = Change_Photo(replacement=change, image=image) 
                    photo.save()     
            # Replacement.objects.create(gubun=gubun, count=count, cost=cost, image=image, bigo=bigo, gigiinfo=gigiinfo2)
            return redirect('gshsapp:gigi_gubun', gigiinfo2.buyproduct.gubun.gubun)
    else:
        changeform = InfogigiChangeForm(initial={'gigiinfo':gigiinfo2})
        formset = ImageFormSet(queryset=Change_Photo.objects.none())
        
    return render(request, 'gshsapp/gigichange.html', {'form': changeform, 'formset': formset})


def InfogigiSuri(request, pk):
    gigiinfo2 = Gigiinfo.objects.get(pk=pk)

    if request.method == 'POST':
        suriform = InfogigiSuriForm(request.POST)
        
        if suriform.is_valid():
            suri = suriform.save()
            for img in request.FILES.getlist('imgs'):
                repair_Photo = Repair_Photo()
                repair_Photo.repair = suri
                repair_Photo.image = img
                repair_Photo.save()

            # problem = form.cleaned_data['problem']
            # result = form.cleaned_data['result']
            # cost = form.cleaned_data['cost']
            # image = form.cleaned_data['image']
            # bigo = form.cleaned_data['bigo']    
           
            # Repair.objects.create(problem=problem, result=result, cost=cost, image=image, bigo=bigo, gigiinfo=gigiinfo2)
            return redirect('gshsapp:gigi_gubun', gigiinfo2.buyproduct.gubun.gubun)
    else:
        form = InfogigiSuriForm(initial={'gigiinfo':gigiinfo2})
        
    return render(request, 'gshsapp/gigisuri.html', {'form': form})
from django import forms
from .models import *


class GigiinfoForm(forms.ModelForm):   
    jaego = forms.CheckboxInput()
    notuse = forms.CheckboxInput()

    def __init__(self, *args, **kwargs):
        self.gigi_gubun = kwargs.pop('gigi_gubun', None)
        super().__init__(*args, **kwargs)  

        if self.instance.pk:
            gigigubun = Gigiinfo.objects.get(pk=self.instance.pk)
            gubun = Gubun.objects.get(gubun=gigigubun.buyproduct.gubun.gubun)
            self.fields['buyproduct']=forms.ModelChoiceField(queryset=gubun.buyproduct.all())

        if self.gigi_gubun:
            gubun = Gubun.objects.get(gubun=self.gigi_gubun)
            self.fields['buyproduct']=forms.ModelChoiceField(queryset=gubun.buyproduct.all())

        self.fields['location']=forms.ModelChoiceField(queryset=Location.objects.all())
        self.fields['user']=forms.ModelChoiceField(required=False, queryset=User.objects.all())
    
    class Meta:
        model = Gigiinfo
        fields = '__all__'   


class InfogigiChangeForm(forms.ModelForm):
    date = forms.CharField(required=False)    
    # bigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gubun']=forms.ModelChoiceField(queryset=Gubun.objects.filter(tablename='replacement'))
    
    class Meta:
        model = Replacement
        fields = '__all__'

class BuseoChangeForm(forms.ModelForm): 
    date = forms.CharField(required=False, widget=forms.DateInput(attrs={'type':'date'}))   
    #bigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    
    # cost = forms.CharField(widget=forms.TextInput(attrs={'onkeyup':'inputNumberFormat(this)'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gubun']=forms.ModelChoiceField(queryset=Gubun.objects.filter(tablename='replacement'))
        
    class Meta:
        model = Replacement
        fields = '__all__'


class InfogigiSuriForm(forms.ModelForm):    
    date = forms.CharField(required=False)
    problem = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))    
    result = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})) 
    # cost = forms.CharField(widget=forms.TextInput(attrs={'onkeyup':'inputNumberFormat(this)'}))   
    # bigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    
    
    class Meta:
        model = Repair
        fields = '__all__'


class Change_PhotoForm(forms.ModelForm):
    class Meta:
        model = Change_Photo
        fields = ('image', )


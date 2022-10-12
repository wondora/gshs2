from django import forms
from .models import *


class GigiinfoForm(forms.ModelForm):   
    ip = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
    jaego = forms.CheckboxInput()
    notuse = forms.CheckboxInput()
    bigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        if self.instance.pk:
            gigigubun = Gigiinfo.objects.get(pk=self.instance.pk)
            gubun = Gubun.objects.get(gubun=gigigubun.buyproduct.gubun.gubun)
            self.fields['buyproduct']=forms.ModelChoiceField(queryset=gubun.buyproduct.all())
       
        self.fields['buyproduct']=forms.ModelChoiceField(queryset=Buyproduct.objects.all())
        self.fields['location']=forms.ModelChoiceField(queryset=Location.objects.all())
        self.fields['user']=forms.ModelChoiceField(required=False, queryset=User.objects.all())
    class Meta:
        model = Gigiinfo
        fields = '__all__'


class InfogigiChangeForm(forms.ModelForm):    
    bigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gubun']=forms.ModelChoiceField(queryset=Gubun.objects.filter(tablename='replacement'))
    
    class Meta:
        model = Replacement
        fields = '__all__'


class InfogigiSuriForm(forms.ModelForm):    
    problem = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    
    result = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    
    bigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))    
    
    class Meta:
        model = Repair
        fields = '__all__'


class Change_PhotoForm(forms.ModelForm):
    
    class Meta:
        model = Change_Photo
        fields = ('image', )


from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

# def hp_validator(value):
#     if len(str(value)) != 10:
#         raise forms.ValidationError('정확한 핸드폰 번호를 입력해주세요.')

# def student_id_validator(value):
#     if len(str(value)) != 8:
#         raise forms.ValidationError('본인의 학번 8자리를 입력해주세요.')

class CsRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CsRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({     
            'class': 'form-control',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
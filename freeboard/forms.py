from django import forms
from .models import Freeboard

class FreeboardWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FreeboardWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'autofocus': True,
            'style': 'background-color: #eee;'
        }),
        self.fields['content'].label = '내용'
        self.fields['content'].widget.attrs.update({
            'style': 'background-color: #eee;padding: 30px;'
        })
    class Meta:
        model = Freeboard
        fields = ['title', 'content', 'top_fixed', 'upload_files']
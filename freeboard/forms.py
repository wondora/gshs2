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
        self.fields['category'].label = '분류'
        self.fields['category'].widget.attrs.update({
            'class': 'form-select form-select-sm',
            'style': "width: 8%; float:left; margin-right:1%; background-color:#eee; margin-bottom: 10px;"
        })

    class Meta:
        model = Freeboard
        fields = ['category','title', 'content', 'top_fixed', 'upload_files']
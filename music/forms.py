from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['post_title'].label = '제목'
        self.fields['post_title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'autofocus': True,
        })
        self.fields['table_num'].widget.attrs.update({

            'class': 'form-control',
            'placeholder': '장르선택',

        })

    class Meta:
        model = Post
        fields = ['table_num', 'writer', 'password', 'post_title',  'post_contents', 'post_file']

        widgets = {
            'writer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
            # 'table_num': forms.TextInput(attrs={'class': 'form-control'}),
            'post_contents' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력해주세요.'}),
            'post_file' : forms.FileInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'username': '닉네임',
            'email': '이메일',
            'password': '패스워드'
        }
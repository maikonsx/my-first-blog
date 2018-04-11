from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

class ContatoForm(forms.Form):
    emissor = forms.EmailField(required=True)
    assunto = forms.CharField(required=True)
    msg = forms.CharField(widget=forms.Textarea)
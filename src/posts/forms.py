from django import forms
from .models import Post,Comment

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content','image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label = "")
    class Meta:
        model = Comment
        fields = ('body',)
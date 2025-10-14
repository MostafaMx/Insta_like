from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        
        model = Blog
        fields = ['title', 'text', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class EditBlogForm(forms.ModelForm):
    image = forms.ClearableFileInput()

    class Meta:
        model = Blog
        fields = ['title', 'text', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


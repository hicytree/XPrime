from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    post = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "What's on your mind today?",
                "class": "form-control",
                "rows": "3",
                "maxlength": "300",
                "required": "True"
            }
        ),
        label=""
    )

    class Meta:
        model = Post
        exclude = ("poster", "likes")

 
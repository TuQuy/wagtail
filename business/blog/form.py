from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_author = kwargs.pop('user_author', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user_author= self.user_author
        comment.post = self.post
        comment.save()
    class Meta:
        model = Comment
        fields = ["body"]
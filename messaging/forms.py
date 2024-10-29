from django import forms
from .models import Message, Comment


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # 送信者やペットはビューで設定


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # コメントの内容だけを投稿できる

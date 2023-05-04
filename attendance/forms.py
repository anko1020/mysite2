from django import forms
from django.contrib.auth.models import User
from .models import Account

class AccountForm(forms.ModelForm):

    class Meta:
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"名前",'email':"メールアドレス"}
        help_texts ={'username':""}
        
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")



from django import forms
from django.forms import widgets
from blog import models
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}), max_length=10, min_length=6,
                               label='用户名')
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}), label='密码')
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}), label='邮箱')


class UserRegForm(forms.ModelForm):
    re_password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}), label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'email', 'telephone']
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            'telephone': forms.TextInput(attrs={"class": "form-control"})
        }
        labels = {
            "username": "用户名",
            "password": "密码",
            "email": "邮箱",
        }

    def clean_username(self):
        reg_user = self.cleaned_data.get('username')
        user = models.UserInfo.objects.filter(username=reg_user).first()
        if not user:
            return reg_user
        else:
            # 把raise错写成return了   导致捕获不了异常报错，搞了很久
            raise ValidationError('用户名已被使用')

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')

        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致，请重新输入！')


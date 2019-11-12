# from django.core.validators import validate_slug
from  django.forms  import widgets
from django  import forms
from captcha.fields import CaptchaField

from index.models import User


##注册
class   RegisterForm(forms.Form):
    '''
    注册验证：
    validators=validate_slug  ##确保值仅包含字母，数字，下划线或连字符的实例
    '''
    email = forms.EmailField(required=True,label='邮箱',widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}),
        max_length=100, error_messages={"required": "邮箱不能为空","invalid": "" })
    pwd = forms.CharField(required=True,label='密码',widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "请输入密码", "value": ""}),
        min_length=8, max_length=50, error_messages={"required": "密码不能为空", "invalid": "密码不能少于8位", "lable": "密码" })
    repwd = forms.CharField(required=True,label='确认密码',widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "请确认密码", "value": "", }),
        min_length=8, max_length=50, error_messages={"required": "密码不能为空","invalid": "密码不能少于8位","lable": "确认密码"})
    ##验证码
    captcha = CaptchaField(label='',error_messages={"invalid":'验证码错误'})
    def clean(self):

        # 用户名
        try:
                email = self.cleaned_data['email']
        except Exception as e:
            print('except: ' + str(e))
            raise forms.ValidationError("邮箱格式错误")

        # 登录验证(邮箱去重)，查看邮箱是否存在
        is_email_exist = User.objects.filter(email=email).exists()
        #is_username_exist = User.objects.filter(username=username).exists()
        if  is_email_exist:
            raise forms.ValidationError("该邮箱已被注册")

        # 密码
        try:
            pwd = self.cleaned_data['pwd']
        except Exception as e:
            print('except: ' + str(e))
            raise forms.ValidationError("请输入至少8位密码")

        return self.cleaned_data
##登陆
class   LoginForm(forms.Form):
    email = forms.EmailField(required=True,label='邮箱',widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}),
        max_length=100, error_messages={"required": "邮箱不能为空","invalid": "" })
    pwd = forms.CharField(required=True,label='密码',widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "请输入密码", "value": ""}),
        min_length=8, max_length=50, error_messages={"required": "密码不能为空", "lable": "密码" })
    def clean(self):

        # 用户名
        try:
                email = self.cleaned_data['email']
        except Exception as e:
            print('except: ' + str(e))
            raise forms.ValidationError("邮箱格式错误")

        # 登录验证(邮箱去重)，查看邮箱是否存在
        is_email = User.objects.filter(email=email)
        #is_username_exist = User.objects.filter(username=username).exists()
        if  is_email:
            raise forms.ValidationError("该邮箱还没注册请前往注册")
##修改密码
class    ChangepwdForm(forms.Form):
    oldpwd=forms.CharField(required=True,label='旧密码',widget=forms.PasswordInput(
        attrs={"placeholder": "请输入旧密码"}
    ))
    newpwd=forms.CharField(required=True,label='新密码',widget=forms.PasswordInput(
        attrs={"placeholder": "请输入新密码"}
    ))
    repwd=forms.CharField(required=True,label='新密码',widget=forms.PasswordInput(
        attrs={"placeholder": "请输入新密码"}
    ))
    # def clean(self):
##找回密码
##重置密码
class   ForgetForm(forms.Form):
    email = forms.EmailField(required=True, label='邮箱', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}),
                             max_length=100, error_messages={"required": "邮箱不能为空", "invalid": ""})
    newpwd = forms.CharField(required=True, label='新密码', widget=forms.PasswordInput(
        attrs={"placeholder": "请输入新密码"}
    ))
    repwd = forms.CharField(required=True, label='新密码', widget=forms.PasswordInput(
        attrs={"placeholder": "请输入新密码"}
    ))


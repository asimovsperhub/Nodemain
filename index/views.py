
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mass_mail

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from index.forms import RegisterForm, LoginForm, ChangepwdForm, ForgetForm
from index.models import Photo, News, User, EmailRecord, Foods
from index.send import send_register_email

# send_mass_mail

def  IndexView(request):

    #轮播图显示给前端
    photo=Photo.objects.all().order_by('position')
    #href=Photo.objects.all().order_by('position')
    data={
        'photos':photo,

    }
    ##给前台传入所有的photo数据
    return render(request, 'index.html',context=data)

#用户注册
def  register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if  form.is_valid():##如果提交数据合法
            ##提取前端页面输入的数据
            email=request.POST.get('email',)
            passwd=request.POST.get('pwd',)
            ##实例化用户表
            user_profile=User()
            ##赋值给数据模型
            user_profile.email=email
            user_profile.passwd=passwd
            #新建用户为非活跃用户，可通过验证变为活跃用户
            user_profile.is_active=False
            ##将传入的密码加密
            user_profile.passwd=make_password(passwd)
            ##保存到数据库
            user_profile.save()
            #发送邮箱激活用户
            send_register_email(email,"register")
    else:
        form=RegisterForm()

    return render(request, 'register.html',locals())
##邮箱激活
def ActiveUser(request,active_code):
    ##在数据库中查询用户访问的这个邮箱激活码
    form=LoginForm()
    all_record=EmailRecord.objects.filter(code=active_code)
    if  all_record:
        for cord in all_record:
            ##通过这个邮箱验证码找到EmailRecord的email
            email=cord.email
            ##通过email这个找到User的email(因为先注册后邮箱验证，传的值是同一个email)
            user=User.objects.get(email=email)
            ##将用户的状态改为激活状态
            user.is_active=1
            user.save()
        return render(request,'login.html',locals())   ##locals()显示当前函数所有局部变量
##判断是否激活用户



##登陆
def login(request):
    if  request.method=='POST':
        form=LoginForm(request.POST)
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        # 登录验证(邮箱去重)，查看邮箱是否存在
        is_email = User.objects.filter(email=email)
        # is_username_exist = User.objects.filter(username=username).exists()
        if is_email:
            ##通过email获取数据库中对应的passwd
            check_passwd=((User.objects.filter(email=email).values())[0]).get('passwd')
            ##check_password将输入的密码和数据库中解密的散列密码对比
            if check_password(pwd,check_passwd):

                ##重定向到user（用户中心）
                ##redirect(to, *args, permanent=False, **kwargs),to：url
                #reverse将(view function or pattern name)反向解析为url
                request.session['email']=email
                return redirect("/user/%s" %email)
            else:
                messages.warning(request,'密码错误')
                return redirect(reverse("login"))


        else:
            messages.warning(request,'邮箱未注册，请前往注册')

    else:
        form=LoginForm()
    return  render(request,'login.html',locals())

##用户中心
##限制未登陆用户访问
#@login_required(login_url='login/')   ##重定向的url，可以写参数也可以在settings中配置
def  UserCenter(request,email):


    return render(request, 'user.html',locals())
##修改密码
#@login_required(login_url='login/')
def  changepwd(request):
    email=request.session.get('email','')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        print(oldpwd)
        check_oldpasswd = ((User.objects.filter(email=email).values())[0]).get('passwd')
        if  check_password(oldpwd,check_oldpasswd)  :
            form = ChangepwdForm(request.POST)
            newpwd=request.POST.get('newpwd')
            repwd=request.POST.get('repwd')
            if  newpwd==repwd:
                ##获取该email所有字段信息
                change_pwd=User.objects.get(email=email)
                ##修改新的密码（passwd字段）
                change_pwd.passwd = make_password(newpwd)
                change_pwd.save()
                messages.success(request,'密码修改成功')
            else:
                messages.warning(request,'两次密码不一致')
        else:
            messages.warning(request,'旧密码错误')

    else:
        form = ChangepwdForm()
    return render(request, 'changepwd.html', locals())

##忘记密码

##发送邮箱验证码
#@login_required(login_url='login/')
def pwdforget(request):
    form=ForgetForm(request.POST)
    if  request.method =='POST':
        form = ForgetForm(request.POST)
        email = request.POST.get('email')
        print(email)
        user_email = User.objects.filter(email=email)
        print(user_email)
        if  user_email:
            send_register_email(email,"forget")

    return render(request,'forgetpwd.html',locals())
##重置密码
#@login_required(login_url='login/')
def repasswd(request,repwd_code):
    if  request.method=='POST':
        form = ForgetForm(request.POST)
        newpwd = request.POST.get('newpwd')
        repwd = request.POST.get('repwd')
        all_record = EmailRecord.objects.filter(code=repwd_code)
        if all_record:
            for cord in all_record:
                ##通过这个邮箱验证码找到EmailRecord的email
                email = cord.email
                if newpwd == repwd:
                    ##获取该email所有字段信息
                    change_pwd = User.objects.get(email=email)
                    ##修改新的密码（passwd字段）
                    change_pwd.passwd = make_password(newpwd)
                    change_pwd.save()
                    messages.success(request, '密码修改成功')
                    #修改成功的重定向到login
                    return redirect(reverse('login'))  ##locals()显示当前函数所有局部变量
                else:
                    messages.warning(request, '两次密码不一致')
    else:
        form = ForgetForm()
        return render(request,'repasswd.html',locals())

    # if  request.method =='POST':
    #     email = request.POST.get('email')
    #     print(email)
    #     user_email = User.objects.filter(email=email)
    #     print(user_email)
    #     if  user_email:
    #         send_register_email(email,"forget")
    #         ##通过邮箱和邮件发送类型找到发送时间并倒序(取出最新的验证码信息条)
    #         code=((EmailRecord.objects.filter(email=email)).filter(send_type='forget').order_by('-send_time').values())[0]
    #         ##取出验证码
    #         code_=code.get('code')
    #         ##表单中的code
    #         code=request.POST.get('code')
    #         if  code==code_:
    #             newpwd = request.POST.get('newpwd')
    #             repwd = request.POST.get('repwd')
    #             if newpwd == repwd:
    #                 ##获取该email所有字段信息
    #                 change_pwd = User.objects.get(email=email)
    #                 ##修改新的密码（passwd字段）
    #                 change_pwd.passwd = make_password(newpwd)
    #                 change_pwd.save()
    #                 messages.success(request, '密码修改成功')
    #                 return render(request,'login.html')
    #             else:
    #                 messages.warning(request, '两次密码不一致')
    #         else:
    #             messages.warning(request,'验证码错误')
    #             return render(request,'forgetpwd.html')
    #     else:
    #         form = RegisterForm()
    #         messages.warning(request,'该用户不存在，请前往注册')
    #         return render(request,'register.html',locals())
    # else:
    #     form = ForgetForm()
    #     return render(request,'forgetpwd.html',locals())








##显示用户登陆日志
#@login_required(login_url='login/')
def  login_log(request):
    # 客户端ip
    ##request.META 是一个Python字典，包含了所有本次HTTP请求的Header信息，
    # 比如用户IP地址和用户Agent（通常是浏览器的名称和版本号）
    email=request.session.get('email')
    user = request.user
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    # 如果被访问对象（被访问的网站），使用了透明代理服务器，那x_forwarded_for就是客户端的真实ip所在了
    #
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ##没有使用代理
        ip = request.META.get('REMOTE_ADDR')
    # ip=request.META['REMOTE_ADDR']
    # context={'user':user,'user_agent':user_agent,'ip':ip,'eamil':email}
    ##用locals比较好，locals加载的比较全面
    return render(request,'login_log.html',locals())



##新闻
def  news(request):
    new=News.objects.all().order_by('id')

    data={
        'news':new,
    }
    ##给前台传入所有的news的数据
    return render(request, 'news.html',context=data)


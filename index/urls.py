
from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.IndexView, name='index'),
    path('index/', views.IndexView, name='index'),
    path('login/',views.login,name='login'),
    ##验证码模块
    path('captcha/',include('captcha.urls')),
    path('register/',views.register,name='register'),
    path('news/',views.news,name='news'),
    ##邮箱激活
    path('active/<str:active_code>',views.ActiveUser,name='activeuser'),
    path('user/<str:email>',views.UserCenter,name='user'),
    path('changepwd/',views.changepwd,name='changepwd'),
    path('loginlog/',views.login_log,name='loginlog'),
    path('pwdforget/',views.pwdforget,name='pwdforget'),
    path('repasswd/<str:repwd_code>',views.repasswd,name='repasswd')
    # path('homepage-2.html',views.homeView2,name='home2'),
    # path('about.html',views.aboutView,name='about'),
    # path('news.html',views.newsView,name='news'),
    # path('projects.html',views.projects,name='projects'),
    # path('services.html',views.services,name='services'),
    # path('contact.html',views.contact,name='contact'),
    # path('cart.html',views.cart,name='cart'),
    # path('404.html',views.err,name='404page'),
    # path('single-news.html',views.single,name='single'),
]

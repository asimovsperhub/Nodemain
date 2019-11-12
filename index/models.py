from django.core.mail import send_mass_mail
from django.db import models

# Create your models here.


from django.utils.datetime_safe import datetime

##注册时用户表


"""
主要是通过邮箱注册
send_mass_mail优先于send_mail
"""
##用户表
class   User(models.Model):
    ##自增：主键字段将自动添加AutoField
    # name=models.CharField(max_length=64)
    ##用户id自增且唯一
    user_id=models.AutoField(primary_key=True,verbose_name='用户id')
    ##email必须唯一
    email=models.EmailField(max_length=50,unique=True,verbose_name='邮箱')
    ##用make_passwd加密给长点
    passwd=models.CharField(max_length=100,verbose_name='密码')
    ##是否激活
    is_active=models.BooleanField(default=False)
    phone=models.CharField(max_length=20,default='null')
    headImg=models.ImageField(upload_to='img/headImg',verbose_name='用户头像')
    name=models.CharField(max_length=50,verbose_name='用户名',default=email)
    # ##性别
    GENDER_CHOICES=(
        (0,'null'),
        (1,'Male'),
        (2,'Female')
    )
    ##choices该参数接收一个可迭代的列表或元组（基本单位为二元组）。如果指定了该参数，在实例化该模型时，该字段只能取选项列表中的值。
    gender=models.IntegerField(choices=GENDER_CHOICES,default=0)
    # ##个人，组织
    # TYPE_CHOICES=(
    #     (0,'null'),
    #     (1,'personal'),
    #     (2,'organization')
    # )
    # id_type=models.IntegerField(choices=TYPE_CHOICES,default=0)
    # ##国籍
    # Country_type=models.CharField(max_length=20,default=0)
    # ##证件类型(身份证，护照)
    # DOC_CHOICES=(
    #     (0,'null'),
    #     (1,'SFZ'),
    #     (2,'HZ')
    # )
    # docoument_type=models.IntegerField(choices=DOC_CHOICES,default=0)
    # ##证件照
    # Document_photo=models.ImageField(upload_to='img/ZJZ/',verbose_name='证件照')
    # ##出生日期，如果blank设置为True，该字段允许为空。默认为False
    # brithday=models.DateField()
    # ##证件号码
    # Document_number=models.CharField(max_length=20,default='null')
    # ##过期时间
    # Document_date=models.DateField(default=datetime.now)
    # ##地址
    # address=models.CharField(max_length=50)

##登陆日志
class   Login_log(models.Model):
    # user_id=models.AutoField(verbose_name='日志id')
    ##登陆用户
    user_name=models.CharField(max_length=50)
    ##IP
    ip=models.CharField(max_length=30)
    ##地区
    area=models.CharField(max_length=30)
    ##时间
    time=models.DateTimeField()
    ##操作
    operat=models.CharField(max_length=50)
##邮箱验证码
class   EmailRecord(models.Model):
    code=models.CharField(max_length=20,verbose_name='验证码')
    ##
    email=models.EmailField(max_length=50,verbose_name='邮箱')
    ##验证类型
    send_type=models.CharField(verbose_name='验证码类型',max_length=10,
                               choices=(('register','注册'),('forget','找回密码')))
    send_time=models.DateTimeField(verbose_name='发送时间',default=datetime.now)
    # class   Meta:
    #     verbose_name='邮箱验证'
    #     verbose_name_plural=verbose_name
    # def __str__(self):
    #     return self.code,self.email
##订单信息
class   Trade(models.Model):
    #user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户id')
    subject=models.CharField(max_length=30,verbose_name='商品名称')
    out_trade_no=models.CharField(max_length=30,verbose_name='订单号')
    foods_price=models.FloatField(max_length=10,verbose_name='单价')
    amount=models.IntegerField(verbose_name='商品总数')




#####################################################后台数据模型##########################################

##后台添加轮播图数据模型
class   Photo(models.Model):
    title=models.CharField(max_length=20,verbose_name='轮播图标题')
    href=models.CharField(max_length=150,verbose_name='图片广告链接')
    ##upload_to图片上传后存储的目录，如果不存在则会自动创建
    src=models.ImageField(upload_to="static/img/banner/",verbose_name='图片')
    position=models.IntegerField(verbose_name='顺序',choices=(
        (1,'new'),
        (2,'old')),default=1)
    class   Meta:
        #db_table   指定数据表名称
        db_table='Photo'
        ##复数
        verbose_name='轮播图'
        ##复数->单数
        verbose_name_plural=verbose_name
    ##按照自定义的格式输出内容
    def  __str__(self):
        return self.title
##添加新闻

class   News(models.Model):
    ##
    title=models.CharField(max_length=30,verbose_name='新闻标题')
    header=models.CharField(max_length=50,verbose_name='主题简介')
    text=models.TextField(verbose_name='内容')
    readcount=models.IntegerField(verbose_name='阅读量')
    class   Meta:
        #db_table   指定数据表名称
        db_table='News'
        ##复数
        verbose_name='添加新闻'
        ##复数->单数
        verbose_name_plural=verbose_name
    ##按照自定义的格式输出内容
    def  __str__(self):
        return self.title
##商品信息
class   Foods(models.Model):

    foods_name=models.CharField(max_length=30,verbose_name='商品名称')
    foods_price=models.FloatField(verbose_name='单价')
    foods_img=models.ImageField(upload_to="static/foodsimg/",verbose_name='商品图片')
    foods_mess=models.CharField(max_length=100,verbose_name='商品信息')
    class   Meta:
        db_table='Foods'
        verbose_name='添加商品信息'
    def __str__(self):
        return self.foods_name





if __name__ == '__main__':
    pass

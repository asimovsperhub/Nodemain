from datetime import datetime

import qrcode
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from index.models import User, Foods
from shop.alipay_T import PreCreate, query_order


def ShopView(request):
    foods = Foods.objects.all().order_by('id')
    print(foods)
    data = {
        'foods': foods,
    }
    return render(request, 'shop_index.html', context=data)

def BuyPreCreate(request,subject):
    """
    创建订单并保存到数据库
    :param request:
    :param subject:
    :param amount:
    :return:
    """
    email = request.session.get('email')
    ##判断是否登陆用户
    if email:
        #user_id=User.objects.filter(email)[0].get('id')
        ##前端返回的数据
        ##商品名
        subject=subject
        request.session['subject']=subject
        ##通过subject从数据库中查该商品的单价
        price=Foods.objects.filter(foods_name=subject).values()[0].get('foods_price')
        request.session['price']=price
        ##前端传的数量
        amount=1
        ##订单号：年月日时分秒+user_id，保证唯一性，且每个用户不可能在同一秒订单号相同
        out_trade_no=int(str(datetime.now()).split('.')[0].replace(' ','').replace('-','').replace(':','')+str('001'))
        request.session['out_trade_no']=out_trade_no
        total_amount=price*amount
        request.session['total_amount']=total_amount
        ##先创建订单
        result=PreCreate(subject,out_trade_no,total_amount)
        print(result)
        ##如果订单创建成功则保存到数据库
        if  result:
           print('创建预订单成功')
                # return render(request,'buy.html',locals())


        code_url = result.get('qr_code')  ##qr_code:创建预付订单成功时返回的："qr_code": "https://qr.alipay.com/bax03431ljhokirwl38f00a7"
        img_url = Foods.objects.filter(foods_name=subject).values()[0].get('foods_img')
        if not code_url:
            print('预付订单创建失败：', result.get('msg'))
            return
        else:
            print('预付订单创建成功：', result.get('msg'))
            ##如果时success response的话去执行get_qr_code函数
            qr_codepay(code_url,out_trade_no)  ##生成一个带有qr_code信息的二维码
            # return  code_url
        return render(request,'buy.html',locals())
    else:
        messages.warning(request, '请先登陆')
        return redirect(reverse("login"))

def qr_codepay(code_url,out_trade_no):
    """
    生成二维码
    :param request:
    :return:
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(code_url)  ##二维码所含信息(支付地址等)
    img = qr.make_image()  ##生成二维码图片
    img.save('/Users/apple/PycharmProjects/untitled1/Node_W/static/code/%s.png' %out_trade_no)
    #print('二维码保存成功')
def Shoppay(request,out_trade_no):
    """
    二维码支付
    :param request:
    :return:
    """
    ##把获取到的订单信息的二维码显示给前端
    out_trade_no=request.session.get('out_trade_no')
    subject=request.session.get('subject')
    price=request.session.get('price')

    ##设定支付时间/s
    cancel_time=120
    ##订单轮询及撤销订单
    query_order(out_trade_no,cancel_time)   ## mes   cancel_tiem

    return render(request,'shoppay.html',locals())
# def Query_order(request):



# def Shoppay(request):
#     """
#     PC端支付
#     :param request:
#     :return:
#     """
# #def Shopping(request):
#     subject=request.session.get('subject')
#     print(subject)
#     #out_trade_no=request.session.get('out_trade_no')
#     out_trade_no=20190916064142001
#     print(out_trade_no)
#     total_amount=request.session.get('total_amount')
#     print(total_amount)
#     ##PC支付端返回的数据
#     order_string=PC_pay(subject,out_trade_no,total_amount)
#     return render(request, 'https://openapi.alipay.com/gateway.do?%s' %order_string,)
#
#     #return render(request, 'shoppay.html', locals())

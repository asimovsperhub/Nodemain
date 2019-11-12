import time

import qrcode
from alipay import AliPay



##初始化

##私钥
app_private_key_string=open("/Users/apple/PycharmProjects/untitled1/Node_W/app_private_key.pem").read()
#print(app_private_key_string)
"""
-----BEGIN RSA PRIVATE KEY-----
base64 encoded content
-----END RSA PRIVATE KEY-----
"""
##支付宝公钥
ali_public_key_string=open('/Users/apple/PycharmProjects/untitled1/Node_W/shahe_ali_pubilc_key.pem').read()
#print(ali_public_key_string)
"""
-----BEGIN PUBLIC KEY-----
base64 encoded content
-----END PUBLIC KEY-----

这个是用于将本地私钥转化成pkcs8格式，支付宝将校验公钥正确性

pkcs8 -topk8 -inform PEM -in app_private_key.pem -outform PEM -nocrypt

"""
# def init_alipay_c(appid):
#     """
#     初始化alipay对象
#     :return:
#     """
alipay=AliPay(appid=2016101400681235, ##appid
              app_notify_url=None,   ##默认回调url，需要外网才能跳转，
              app_private_key_string=app_private_key_string,  ##本地私钥

              ##支付宝的公钥，验证支付回传消息时使用,不是自己生成的公钥，这个需要去支付宝上传本地公钥，然后给你生成支付宝公钥
              alipay_public_key_string=ali_public_key_string,
              sign_type="RSA2",  ##RSA 或 RSA2  (当你在支付宝验证过密钥正确性还报不匹配时可以试试换RSA2或RSA)
              debug=True  ##默认False，若开启则使用沙盒环境用True
              )
    # return alipay
"""
AliPay()参数：
def __init__(
        self,
        appid,
        app_notify_url,     ##默认回调url
        app_private_key_path=None,
        app_private_key_string=None,   ##本地私钥
        alipay_public_key_path=None,
        alipay_public_key_string=None,  ##支付宝的公钥，验证支付回传消息时使用
        sign_type="RSA2",               ##加密方式
        debug=False

初始化:
        alipay = AliPay(
          appid="",
          app_notify_url="http://example.com",
          app_private_key_path="",
          alipay_public_key_path="",
          sign_type="RSA2"
        )
注意：

接口基本命名规则
对于一个支付宝的接口，比如alipay.trade.page.pay，则一般可以这么调用接口：alipay.api_alipay_trade_page_pay()
也就是说，我们做了这么一个转换:

 内部函数名 =  api_ + 支付宝接口名.replace(".", "_")

"""

def get_qr_code(code_url):
    """
    生成二维码
    :param code_url:  创建预付订单时生成的code_url
    :return:
    """
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(code_url) ##二维码所含信息(支付地址等)
    img=qr.make_image()   ##生成二维码图片
    img.save('/Users/apple/PycharmProjects/untitled1/Node_W/static/qr_test_ali.png')
    print('二维码保存成功')
def PreCreate_code(subject,out_trade_no:int,total_amount:int or float):
    """
    创建二维码预付订单；alipay.trade.precreate
    :param subject:         商品名称
    :param out_trade_no:    订单号
    :param total_amount:    价格
    :return:


    success response  = {
          "alipay_trade_precreate_response": {
            "msg": "Success",
            "out_trade_no": "out_trade_no17",
            "code": "10000",
            "qr_code": "https://qr.alipay.com/bax03431ljhokirwl38f00a7"
          },
          "sign": ""
        }

        failed response = {
          "alipay_trade_precreate_response": {
            "msg": "Business Failed",
            "sub_code": "ACQ.TOTAL_FEE_EXCEED",
            "code": "40004",
            "sub_msg": "订单金额超过限额"
          },
          "sign": ""
        }
    """
    result=alipay.api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount)
    print('返回值',result)
    code_url=result.get('qr_code')  ##qr_code:创建预付订单成功时返回的："qr_code": "https://qr.alipay.com/bax03431ljhokirwl38f00a7"

    if  not code_url:
        print('预付订单创建失败：',result.get('msg'))
        return
    else:
        print('预付订单创建成功：',result.get('msg'))
        ##如果时success response的话去执行get_qr_code函数
        get_qr_code(code_url)   ##生成一个带有qr_code信息的二维码
        #return  code_url

def PreCreate(subject,out_trade_no:int,total_amount:int or float):
    """
    创建预付订单

    :param subject:
    :param out_trade_no:
    :param total_amount:
    :return:
    """
    result = alipay.api_alipay_trade_precreate(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount)
    print('创建预付订单成功', result)
    return result

def PC_pay(subject,out_trade_no:int,total_amount:int or float):
    """

    :param subject:
    :param out_trade_no:
    :param total_amount:
    :return:
    """
    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        ##支付页面的url
        return_url="http://127.0.0.1:8000/shop/pay/",
        # notify_url="https://example.com/notify" # 回调url，可选, 不填则使用默认notify url
    )
    return order_string
def query_order(out_trade_no:int,cancel_time:int):
    """
    订单状态查询：alipay.trade.query
    :param out_trade_no:  商户订单号
    :param cancel_time:   设置支付时间
    :return:

     response:
    "trade_status": "TRADE_SUCCESS",
    "code": "10000",
    """
    print('预付订单已创建，请在%s秒内支付' %cancel_time)
    ##

    """
    轮询设置的支付时间每次等1s
    """
    for i  in range(cancel_time):
        print('还有：%s s支付时间' %cancel_time)
        time.sleep(1)
        ##订单查询
        result=alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if  result.get("trade_status","")=="TRADE_SUCCESS":
            print('订单已支付')
            print('订单查询返回值：',result)
            break
        cancel_time-=1
        if cancel_time<=0:
            ##如果超过支付时间，执行cancel_order函数 ，撤销订单
            cancel_order(out_trade_no,cancel_time)
            mes='已超过预计时间，订单已撤销'
            return mes
        return cancel_time
def cancel_order(out_trade_no:int,cancel_time=None):
    """
    撤销订单：alipay.trade.cancel
    :param out_trade_no:    商户订单号
    :param cancel_time:     设置的支付时间
    :return:

    assert (out_trade_no is not None) or (trade_no is not None),\
            "Both trade_no and out_trade_no are None"
    订单号out_trade_no不能为空
    """
    result=alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
    resp_status=result.get('msg')
    if  resp_status=="Success":  #撤销成功

            if cancel_time==0:
                print('%s秒还未支付订单，订单已被取消'  %cancel_time)
    else:
        print('请求失败',resp_status)

def roll_refund(out_trade_no:str or int,refund_amount:int  or  float,out_request_no:str):

    """
    退款操作：alipay.trade.refund
    :param out_trade_no:        商户订单号
    :param refund_amount:       退款金额，小于等于订单金额
    :param out_request_no:      商户自定义参数，用来标识该次退款请求的唯一性,可使用 out_trade_no_退款金额*100 的构造方式
    :return:
    """
    result=alipay.api_alipay_trade_refund(out_trade_no=out_trade_no,
                                          refund_amount=refund_amount,
                                          out_request_no=out_request_no)
    if  result['code']=="10000":#调用成功则返回result
        return result
    else:
        return result['msg']  #接口调用失败则返回msg
def fastpay_refund(out_trade_no,out_request_no):
    """
    统一收单交易退款查询：alipay.trade.fastpay.refund.query
    :param out_trade_no:商户订单号
    :param out_request_no:商户自定义的单次退款请求标识符
    :return:
    """
    result=alipay.api_alipay_trade_fastpay_refund_query(out_trade_no=out_trade_no,out_request_no=out_request_no)
    if  result['code']=='10000':
        return result
    else:
        return result['msg']

 #alipay.trade.query，电脑端若没有回调url可通过此接口进行交易查询
 #def
if __name__ == '__main__':
    ##创建预订单
    ##商品名称
    subject='蚂蚁矿机'
    ##订单号
    out_trade_no=int(time.time())  ##将当前时间的时间戳转化为整型用做订单号
    ##价格
    total_amount=999
    PreCreate(subject=subject,out_trade_no=out_trade_no,total_amount=total_amount)

    ##订单查询
    ##当你设置支付时间的话，时间过了，二维码会失效
    cancel_time=30
    query_order(out_trade_no,cancel_time)




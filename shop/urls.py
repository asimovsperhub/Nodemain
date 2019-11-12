from django.urls import path

from . import views

urlpatterns = [
    ##商城主页
    path('', views.ShopView, name='shop'),
    #购买页面
    path('buy/<str:subject>/',views.BuyPreCreate,name='buy'),
    # 支付页面
    path('pay/<int:out_trade_no>', views.Shoppay, name='pay'),
]
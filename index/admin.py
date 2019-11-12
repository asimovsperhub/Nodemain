from django.contrib import admin

# Register your models here

from  . models import *

##轮播图
class   PhotoAdmin(admin.ModelAdmin):
    ##定义后台列表展示的字段
    list_display = ['title','position','src','href']
    ##定义后台允许搜索的字段
    search_fields = ['title']
    ##后台过滤器，筛选字段
    list_filter = ['position']

# admin.register(Photo,PhotoAdmin)数据模型，admin类
#注册后台功能
admin.site.register(Photo,PhotoAdmin)

class   NewAdmin(admin.ModelAdmin):
    list_display = ['id','title','header','text','readcount']
    search_fields = ['title']
    list_filter = ['id']
admin.site.register(News,NewAdmin)

# class   FoodsAdmin(admin.ModelAdmin):
#     list_display = ['id','foods_name','foods_price','foods_img','foods_mess']
#     search_fields = ['foods_name']
#     list_filter = ['id']
# admin.site.register(Foods,FoodsAdmin)
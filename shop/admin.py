from django.contrib import admin

# Register your models here.
from index.models import Foods


class   FoodsAdmin(admin.ModelAdmin):
    list_display = ['id','foods_name','foods_price','foods_img','foods_mess']
    search_fields = ['foods_name']
    list_filter = ['id']
admin.site.register(Foods,FoodsAdmin)
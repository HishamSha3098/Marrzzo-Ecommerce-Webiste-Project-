from django.contrib import admin
from .models import userprofile,Address,Message

# Register your models here.
class Userprofileadmin(admin.ModelAdmin):
    list_display = ['user_name','name','phone','address','postcode','state','city','email','country','phone2','image']
admin.site.register(userprofile,Userprofileadmin)
admin.site.register(Address)
admin.site.register(Message)


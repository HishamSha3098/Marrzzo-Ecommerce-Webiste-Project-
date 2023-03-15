from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.BigIntegerField()


class userprofile(models.Model) :
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(blank=True,max_length=50)
    phone = models.CharField(blank=True,max_length=50)
    address = models.CharField(blank=True,max_length=50)
    postcode = models.CharField(blank=True,max_length=15)
    state = models.CharField(blank=True,max_length=50)
    city = models.CharField(blank=True,max_length=50)
    email = models.EmailField(blank=True,max_length=250)
    country = models.CharField(blank=True,max_length=50)
    phone2 = models.CharField(blank=True,max_length=50)
    image = models.ImageField(upload_to='images/users/', default='images/users/pngwing.com_3.png')
    primary_address=models.BooleanField(default=True)


    def __str__(self):
        return self.user.username
    def user_name(self):
        return self.user.first_name+ '' + self.user.last_name + '['+self.user.username+']'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'image'
    

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    address=models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(blank=True,max_length=50,null=True)
    city=models.CharField(max_length=20,null=True)
    state=models.CharField(max_length=20,null=True)
    country=models.CharField(max_length=20,null=True)
    post_code=models.CharField(blank=True,max_length=50,null=True)
    primary_address=models.BooleanField(default=True)
    order_note = models.CharField(max_length=500,default='',null=True)    

    def __str__(self):
        return self.name
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']




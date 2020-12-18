from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')

        user = self.model(username=username,email = self.normalize_email(email))
        user.set_password(password)
        user.save() 
        return user

    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user




class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100,unique=True,db_index=True)
    email = models.EmailField(max_length=255,unique=True,db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default='email')
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = [ 
        'email'
    ]


    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access': str(refresh.access_token),
        }



class Profile(models.Model):
    owner = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=200,null=True,blank=True)
    codeforces = models.CharField(max_length=50,null=True,blank=True)
    codechef = models.CharField(max_length=50,null = True,blank=True,default=" ")
    spoj = models.CharField(max_length=50,null = True,blank=True,default=" ")
    atcoder = models.CharField(max_length=50,null = True,blank=True,default=" ")
    uva_handle = models.CharField(max_length=50,null = True,blank=True,default=" ")
    uva_id = models.CharField(max_length=50,null = True,blank=True,default=" ")
    created_at = models.DateTimeField(auto_now_add=True,null = True,blank=True)
    updated_at = models.DateTimeField(auto_now = True,null = True,blank=True)


    def __str__(self):
        return str(self.owner) + "'s Profile"

    @receiver(post_save, sender=User)
    def create_Profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance)
    

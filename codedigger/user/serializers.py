from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import User,Profile
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed,ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes,smart_str,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_decode
from .handle_validator import *




class GuruSerializer(serializers.ModelSerializer):
    gurus = serializers.CharField(max_length=300)
    class Meta:
        model = Profile
        fields = ['gurus']
    
    def validate(self,attrs):
        return attrs
    
    def update(self , instance , validated_data):
        print('LOL')
        print(validated_data)
        instance.gurus = validated_data.get('gurus' , instance.gurus)
        instance.save()
        return instance



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password']
         
    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)
    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3,read_only=True)
    password = serializers.CharField(max_length = 68,min_length = 6,write_only=True)
    username = serializers.CharField(max_length = 68)
    tokens = serializers.SerializerMethodField()
    first_time_login = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    def get_first_time_login(self,obj):
        qs = Profile.objects.get(owner__username = obj['username'])
        if qs.name is None:
            return True
        return False



    class Meta:
        model = User
        fields = ['id','username','email','password','tokens','first_time_login']

    def validate(self,attrs):
        username =  attrs.get('username','')
        password =  attrs.get('password','')
        user_obj_email = User.objects.filter(email=username).first()
        user_obj_username = User.objects.filter(username=username).first()
        if user_obj_email:
            # if user_obj_email.is_authenticated:
            #     raise AuthenticationFailed('Already Logged In')
            user = auth.authenticate(username = user_obj_email.username,password=password)
            if user_obj_email.auth_provider != 'email':
                raise AuthenticationFailed(
                    detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
            if not user:
                raise AuthenticationFailed('Invalid credentials. Try again')
            if not user.is_active:
                raise AuthenticationFailed('Account disabled. contact admin')
            if not user.is_verified:
                raise AuthenticationFailed('Email is not verified')
            return {
                'email' : user.email,
                'username' : user.username,
                'tokens': user.tokens
            }
            return super().validate(attrs)
        if user_obj_username:
            # if user_obj_username.is_authenticated:
            #     raise AuthenticationFailed('Already Logged In')
            user = auth.authenticate(username = username,password=password)
            if not user:
                raise AuthenticationFailed('Invalid credentials. Try again')
            if not user.is_active:
                raise AuthenticationFailed('Account disabled. contact admin')
            if not user.is_verified:
                raise AuthenticationFailed('Email is not verified')
            return {
                'email' : user.email,
                'username' : user.username,
                'tokens': user.tokens
            }
            return super().validate(attrs)
        raise AuthenticationFailed('Invalid credentials. Try again')
        

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

def check_cf(value):
    if value is None:
        raise serializers.ValidationError('This fiels is required')
    if not check_handle_cf(value):
        raise serializers.ValidationError('The given handle does not exist')

def check_spoj(value):
    if value is not None and not check_handle_spoj(value):
        raise serializers.ValidationError('The given handle does not exist')

def check_codechef(value):
    if value is not None and not check_handle_codechef(value):
        raise serializers.ValidationError('The given handle does not exist')

def check_atcoder(value):
    if value is not None and not check_handle_atcoder(value):
        raise serializers.ValidationError('The given handle does not exist')

def check_uva_handle(value):
    if value is not None and not check_handle_uva(value):
        raise serializers.ValidationError('The given handle does not exist')




class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[required])
    codeforces = serializers.CharField(validators=[check_cf])
    spoj = serializers.CharField(validators=[check_spoj],allow_blank = True)
    codechef = serializers.CharField(validators=[check_codechef],allow_blank = True)
    atcoder = serializers.CharField(validators=[check_atcoder],allow_blank = True)
    uva_handle = serializers.CharField(validators=[check_uva_handle],allow_blank = True)
    password = serializers.CharField(max_length = 68,min_length = 6,write_only=True)

    def validate(self,attrs):
        username = self.context.get('user')
        password = attrs.get('password')
        if password.strip() is None:
            return super().validate(attrs)
        qs = User.objects.filter(username=username).first()
        qs.set_password(password)
        qs.save()
        return super().validate(attrs)


    class Meta:
        model = Profile
        fields = ['name','codeforces','codechef','atcoder','spoj','uva_handle','password']


    
    


class RequestPasswordResetEmailSeriliazer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

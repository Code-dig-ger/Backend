from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import User, Profile, UserFriends
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_decode
from .handle_validator import *
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
import requests, json
from lists.models import Solved
from .exception import *
import re


class GuruSerializer(serializers.ModelSerializer):
    guru = serializers.CharField(max_length=300)

    class Meta:
        model = Profile
        fields = ['guru']

    def validate(self, attrs):

        handle = attrs.get('guru', '')
        res = requests.get('https://codeforces.com/api/user.info?handles=' +
                           handle)

        if res.status_code >= 500:
            raise ValidationException('Codeforces API is not working!')
        elif res.status_code >= 400:
            raise ValidationException(handle +
                                      ' is not a valid Codeforces handle')

        res = res.json()

        if res['status'] != "OK":
            raise ValidationException(handle +
                                      ' is not a valid Codeforces handle')

        return attrs

    def add(self, instance, validated_data):

        if re.search(',' + validated_data.get('guru') + ',', instance.gurus,
                     re.IGNORECASE):
            raise ValidationException((validated_data.get('guru')) +
                                      " is already present in list")

        if len(instance.gurus.split(',')[1:-1]) >= 10:
            raise ValidationException(
                'You cannot add more mentors in your list. Delete Some. Use it wisely.'
            )

        instance.gurus = instance.gurus + validated_data.get('guru') + ','

        if len(instance.gurus) > 300:
            raise ValidationException(
                'You cannot add more mentors in your list. Delete Some. Use it wisely.'
            )

        instance.save()
        return instance

    def delete(self, instance, data):

        if data.get('guru') == None:
            raise ValidationException('guru field is required')

        if re.search(',' + data.get('guru') + ',', instance.gurus,
                     re.IGNORECASE):
            instance.gurus = re.sub(',' + data['guru'] + ',',
                                    ',',
                                    instance.gurus,
                                    flags=re.IGNORECASE)
            instance.save()
            return instance
        else:
            raise ValidationException((data.get('guru')) +
                                      " is not present in list")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,
                                     min_length=6,
                                     write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        # if not username.isalnum():
        #     raise ValidationException("The username should only contain alphanumeric characters")
        if re.match(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{1,75}(?<![-._])$',
                    username) is None:
            raise ValidationException("Username is invalid")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    class Meta:
        fields = ['email']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=68,
                                     min_length=6,
                                     write_only=True)
    username = serializers.CharField(max_length=100)
    tokens = serializers.SerializerMethodField()
    first_time_login = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def get_first_time_login(self, obj):
        qs = Profile.objects.get(owner__username=obj['username'])
        if qs.name is None:
            return True
        return False

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'tokens', 'first_time_login'
        ]

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user_obj_email = User.objects.filter(email=username).first()
        user_obj_username = User.objects.filter(username=username).first()
        if user_obj_email:
            user = auth.authenticate(username=user_obj_email.username,
                                     password=password)
            if user_obj_email.auth_provider != 'email':
                raise AuthenticationException(
                    'Please continue your login using ' +
                    user_obj_email.auth_provider)
            if not user:
                raise AuthenticationException('Invalid credentials. Try again')
            if not user.is_active:
                raise AuthenticationException(
                    'Account disabled. contact admin')
            if not user.is_verified:
                email = user.email
                token = RefreshToken.for_user(user).access_token
                current_site = self.context.get('current_site')
                relative_link = reverse('email-verify')
                absurl = 'https://' + current_site + relative_link + "?token=" + str(
                    token)
                email_body = {}
                email_body['username'] = user.username
                email_body['message'] = 'Use link below to verify your email'
                email_body['link'] = absurl
                data = {
                    'email_body': email_body,
                    'email_subject': 'Verify your email',
                    'to_email': user.email
                }
                Util.send_email(data)
                raise AuthenticationException(
                    'Email is not verified, A Verification Email has been sent to your email address'
                )
            return {
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens
            }
            return super().validate(attrs)
        if user_obj_username:
            user = auth.authenticate(username=username, password=password)
            if not user:
                raise AuthenticationException('Invalid credentials. Try again')
            if not user.is_active:
                raise AuthenticationException(
                    'Account disabled. contact admin')
            if not user.is_verified:
                email = user.email
                token = RefreshToken.for_user(user).access_token
                current_site = self.context.get('current_site')
                relative_link = reverse('email-verify')
                absurl = 'https://' + current_site + relative_link + "?token=" + str(
                    token)
                email_body = {}
                email_body['username'] = user.username
                email_body['message'] = 'Use link below to verify your email'
                email_body['link'] = absurl
                data = {
                    'email_body': email_body,
                    'email_subject': 'Verify your email',
                    'to_email': user.email
                }
                Util.send_email(data)
                raise AuthenticationException(
                    'Email is not verified, A Verification Email has been sent to your email address'
                )
            return {
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens
            }
            return super().validate(attrs)
        raise AuthenticationException('Invalid credentials. Try again')


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    codeforces = serializers.CharField()
    spoj = serializers.CharField(allow_blank=True,
                                 allow_null=True,
                                 required=False)
    codechef = serializers.CharField(allow_blank=True,
                                     allow_null=True,
                                     required=False)
    atcoder = serializers.CharField(allow_blank=True,
                                    allow_null=True,
                                    required=False)
    uva_handle = serializers.CharField(allow_blank=True,
                                       allow_null=True,
                                       required=False)

    class Meta:
        model = Profile
        fields = [
            'name',
            'codeforces',
            'codechef',
            'atcoder',
            'spoj',
            'uva_handle',
        ]

    def validate_codeforces(self, value):
        user = self.context.get('user')
        curr_user = User.objects.get(username=user)
        if value != Profile.objects.get(owner=curr_user).codeforces:
            cf_status = check_handle_cf(value)
            if cf_status == 2:
                Solved.objects.filter(user=curr_user,
                                      problem__platform='F').delete()
            elif cf_status:
                raise ValidationException(
                    'It seems Codeforces API is not working! Please Wait until it is working perfect.'
                )
            else:
                raise ValidationException(
                    'The given codeforces handle does not exist')
        return value

    def validate_codechef(self, value):
        user = self.context.get('user')
        curr_user = User.objects.get(username=user)
        if value != Profile.objects.get(owner=curr_user).codechef:
            if check_handle_codechef(value):
                Solved.objects.filter(user=curr_user,
                                      problem__platform='C').delete()
            else:
                raise ValidationException(
                    'The given codechef handle does not exist')
        return value

    def validate_atcoder(self, value):
        user = self.context.get('user')
        curr_user = User.objects.get(username=user)
        if value != Profile.objects.get(owner=curr_user).atcoder:
            if check_handle_atcoder(value):
                Solved.objects.filter(user=curr_user,
                                      problem__platform='A').delete()
            else:
                raise ValidationException(
                    'The given atcoder handle does not exist')
        return value

    def validate_spoj(self, value):
        user = self.context.get('user')
        curr_user = User.objects.get(username=user)
        if value != Profile.objects.get(owner=curr_user).spoj:
            if check_handle_spoj(value):
                Solved.objects.filter(user=curr_user,
                                      problem__platform='S').delete()
            else:
                raise ValidationException(
                    'The given spoj handle does not exist')
        return value

    def validate_uva_handle(self, value):
        user = self.context.get('user')
        curr_user = User.objects.get(username=user)
        if value != Profile.objects.get(owner=curr_user).uva_handle:
            if check_handle_uva(value):
                Solved.objects.filter(user=curr_user,
                                      problem__platform='U').delete()
            else:
                raise ValidationException(
                    'The given UVA handle does not exist')
        return value


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
    password = serializers.CharField(min_length=6,
                                     max_length=68,
                                     write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

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
                raise AuthenticationException('The reset link is invalid')

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationException('The reset link is invalid')
        return super().validate(attrs)


class PasswordChangeSerializer(serializers.Serializer):
    old_pass = serializers.CharField(max_length=68,
                                     min_length=6,
                                     required=True)
    new_pass = serializers.CharField(max_length=68,
                                     min_length=6,
                                     required=True)

    class Meta:
        fields = ['old_pass', 'new_pass']


# Friends Serializer Starts


class SendFriendRequestSerializer(serializers.Serializer):

    to_user = serializers.CharField(max_length=100)

    class Meta:
        fields = ['to_user']


class RemoveFriendSerializer(serializers.Serializer):

    user = serializers.CharField(max_length=100)

    class Meta:
        fields = ['user']


class AcceptFriendRequestSerializer(serializers.Serializer):

    from_user = serializers.CharField(max_length=100)

    class Meta:
        fields = ['from_user']


class FriendsShowSerializer(serializers.Serializer):

    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_username(self, obj):

        if self.context.get('by_to_user'):
            return obj.to_user.username
        else:
            return obj.from_user.username

    def get_name(self, obj):

        if self.context.get('by_to_user'):
            return Profile.objects.get(owner=obj.to_user).name
        else:
            return Profile.objects.get(owner=obj.from_user).name

    class Meta:
        model = UserFriends
        fields = ['username', 'name']


# Friends Serializer Ends

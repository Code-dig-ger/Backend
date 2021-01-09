from django.shortcuts import render
from rest_framework import generics,status,permissions,views
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    RequestPasswordResetEmailSeriliazer,
    RequestPasswordResetEmailSeriliazer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Profile
from lists.models import Solved
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings  
import jwt , json
from .permissions import IsOwner
from rest_framework.generics import RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import UpdateAPIView,ListAPIView,ListCreateAPIView
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import authenticate
from .handle_validator import *
# Profile
from .profile import get_atcoder_profile, get_spoj_profile, get_uva_profile, get_codechef_profile, get_codeforces_profile
from codeforces.models import user as CodeforcesUser
from codeforces.serializers import UserSerializer as CodeforcesUserSerializer

# Friends
from .serializers import SendFriendRequestSerializer , RemoveFriendSerializer , AcceptFriendRequestSerializer , FriendsShowSerializer
from .models import UserFriends

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = ['https']


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer]

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        relative_link = reverse('email-verify')


        absurl = 'https://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username + '. Use link below to verify your email \n' + absurl
        data = {'email_body' : email_body,'email_subject' : 'Verify your email','to_email' : user.email}
        Util.send_email(data)
        return Response(user_data,status = status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email' : 'Successfully activated'},status = status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email' : 'Activation link expired'},status = status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'email' : 'Invalid token, Request New One'},status = status.HTTP_400_BAD_REQUEST)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context = {'current_site' : get_current_site(request).domain})
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data,status = status.HTTP_200_OK)

class CheckAuthView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args, **kwargs):
        return Response({'status' : 'ok'},status=status.HTTP_200_OK)


class SendVerificationMail(views.APIView):
    def get(self,request,*args, **kwargs):
        email = request.data.get('email',None)
        if email is None:
            return Response({'status' : 'Email not provided'},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'https://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.username + '. Use link below to verify your email \n' + absurl
        data = {'email_body' : email_body,'email_subject' : 'Verify your email','to_email' : user.email}
        Util.send_email(data)
        return Response({'status' : 'A Verification Email has been sent'},status = status.HTTP_200_OK)


class ProfileGetView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    queryset = Profile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)



class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    queryset = Profile.objects.all()
    lookup_field = "owner_id__username"

    def get_serializer_context(self,**kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_update(self,serializer):
        uva = self.request.data['uva_handle']
        if not uva:
            pass
        return serializer.save(uva_id = get_uva(uva))

class ChangePassword(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        data = request.data
        old_pass = data.get('old_pass',None)
        new_pass = data.get('new_pass',None)
        if old_pass is None or new_pass is None:
            return Response({'status' : 'Either the old or new password was not provided'},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=self.request.user.username,password=old_pass)
        if new_pass == old_pass:
            return Response({'status' : "The new password is same as the old password"},status=status.HTTP_400_BAD_REQUEST)
        if len(new_pass) < 6:
            return Response({'status' : "The password is too short, should be of minimum length 6"},status=status.HTTP_400_BAD_REQUEST)
        if user is None:
            return Response({'status' : "Wrong Password"},status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_pass)
        user.save()
        return Response({'status' : "Password Change Complete"},status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'https://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')
        print(redirect_url)

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                # if redirect_url and len(redirect_url) > 3:
                #     return CustomRedirect(redirect_url+'?token_valid=False')
                # else:
                #     return CustomRedirect(os.getenv('FRONTEND_URL', '')+'?token_valid=False')
                return Response({'error' : 'Token is invalid. Please request a new one'})
            return Response({'success' : True,'message' : 'Credentials valid' , 'uidb64' : uidb64,'token' : token})
            # if redirect_url and len(redirect_url) > 3:
            #     return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            # else:
            #     return CustomRedirect(os.getenv('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            # try:
            #     if not PasswordResetTokenGenerator().check_token(user):
            #         return CustomRedirect(redirect_url+'?token_valid=False')
                    
            # except UnboundLocalError as e:
            #     return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error' : 'Token is invalid. Please request a new one'})



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


# Profile View 

class UserProfileGetView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    def get(self , request , username):

        try :
            user = User.objects.get(username = username)
        except User.DoesNotExist : 
            return Response({'status' : 'FAILED' , 'error' : 'Requested User doesn\'t exists in our database. Register Now! :)'})

        profile = Profile.objects.get(owner = user)

        if profile.codeforces == None:
            return Response({'status' : 'FAILED' , 'error' : 'Requested User haven\'t activated his/her account. :( '})

        ermsg = "You haven\'t entered {} handle in your Profile. Update Profile Now! "

        data = {}

        if request.GET.get('platform') == None: 
            # Send Profile 
            data = ProfileSerializer(profile).data
            data['username'] = user.username
            data['email'] = user.email
            if request.user.is_authenticated :
                if request.user.username == username:
                    data['about_user'] = 'Logged In User Itself'
                else :
                    # Check for friends 
                    if UserFriends.objects.filter(status = True , to_user = request.user , from_user = User.objects.get(username = username)).exists() :
                        data['about_user'] = 'Friends'
                    elif UserFriends.objects.filter(status = True , to_user = User.objects.get(username = username) , from_user = request.user).exists() :
                        data['about_user'] = 'Friends'
                    elif UserFriends.objects.filter(status = False , to_user = User.objects.get(username = username) , from_user = request.user).exists() :
                        data['about_user'] = 'Request Sent'
                    elif UserFriends.objects.filter(status = False , to_user = request.user , from_user = User.objects.get(username = username)).exists() :
                        data['about_user'] = 'Request Received'
                    else :
                        data['about_user'] = 'Stalking'
            else :
                data['about_user'] = 'Not Authenticated'


        elif request.GET.get('platform') == "codeforces" :

            try :
                codeforces_user = CodeforcesUser.objects.get(handle = profile.codeforces)
            except CodeforcesUser.DoesNotExist :
                codeforces_user = None

            codeforces_user , codeforces_data = get_codeforces_profile(profile.codeforces , codeforces_user)
            if codeforces_user != None :
                data = CodeforcesUserSerializer(codeforces_user).data
                data['status'] = codeforces_data['status'] 
                data['contribution'] = codeforces_data['contribution']
                data['avatar'] = codeforces_data['avatar']
                data['lastOnlineTimeSeconds'] = codeforces_data['lastOnlineTimeSeconds']
                data['friendOfCount'] = codeforces_data['friendOfCount'] 
            else :
                data = codeforces_data 

        elif request.GET.get('platform') == "codechef" :
            if profile.codechef != "" and profile.codechef != None:
                data = get_codechef_profile(profile.codechef)
            else :
                return Response({'status' : 'FAILED' , 'error' : ermsg.format('codechef')})

        elif request.GET.get('platform') == "atcoder" :
            if profile.atcoder != "" and profile.atcoder != None:
                data = get_atcoder_profile(profile.atcoder)
            else :
                return Response({'status' : 'FAILED' , 'error' : ermsg.format('atcoder')})

        elif request.GET.get('platform') == "uva" :
            if profile.uva_handle != "" and profile.uva_handle != None:
                data = get_uva_profile(profile.uva_id , profile.uva_handle)
            else :
                return Response({'status' : 'FAILED' , 'error' : ermsg.format('uva')})

        elif request.GET.get('platform') == "spoj" :
            if profile.spoj != "" and profile.spoj != None:
                data = get_spoj_profile(profile.spoj)
            else :
                return Response({'status' : 'FAILED' , 'error' : ermsg.format('spoj')})
        else :
            return Response({'status' : 'FAILED' , 'error' : 'Invalid GET Request'})

        return Response({'status' : 'OK' , 'result' : data})
        

# Friends Related View Start

class SendFriendRequest(generics.GenericAPIView):

    serializer_class = SendFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        to_user = request.data["to_user"]

        # Check this username is Valid or Not 

        if Profile.objects.get(owner = request.user).codeforces == "" or Profile.objects.get(owner = request.user).codeforces == None :
            return Response({'status': 'FAILED', 'error' : 'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '})

        if request.user.username == to_user :
            return Response({'status' : 'FAILED' , 'error' : 'You cannot send a friend request to yourself.'}) 

        try: 
            to_user = User.objects.get(username = to_user , is_verified = True)
            if Profile.objects.get(owner = to_user).codeforces == "" or Profile.objects.get(owner = to_user).codeforces == None :
                return Response({'status' : 'FAILED' , 'error' : 'Requested User haven\'t activated his account.'})
        except User.DoesNotExist :
            return Response({'status' : 'FAILED' , 'error' : 'Requested User Doesn\'t Exists in our database.'})

        # Check whether this have sent a request already or not 
        try:
            status = UserFriends.objects.get(from_user = request.user, to_user = to_user)
            if status.status == True:
                return Response({'status' : 'FAILED' , 'error' : 'You are already Friends.'})
            else :
                return Response({'status' : 'FAILED' , 'error' : 'You have already Sent a Friend Request to this User.'})
        except UserFriends.DoesNotExist:
            # Check for Opposite 

            try : 
                status = UserFriends.objects.get(from_user = to_user, to_user = request.user)
                if status.status == True:
                    return Response({'status' : 'FAILED' , 'error' : 'You are already Friends.'})
                else :
                    status.status = True
                    return Response({'status' : 'OK' , 'result' : 'You are now Friends'})

            except UserFriends.DoesNotExist:
                UserFriends.objects.create(from_user = request.user , to_user = to_user , status = False)
                return Response({'status' : 'OK' , 'result' : 'Friend Request Sent!'})

class RemoveFriend(generics.GenericAPIView):

    serializer_class = RemoveFriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        if Profile.objects.get(owner = request.user).codeforces == "" or Profile.objects.get(owner = request.user).codeforces == None :
            return Response({'status': 'FAILED', 'error' : 'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '})

        user = request.data["user"]

        # Check this username is Valid or Not 
        try: 
            user = User.objects.get(username = user , is_verified = True)
            if Profile.objects.get(owner = user).codeforces == "" or Profile.objects.get(owner = user).codeforces == None :
                return Response({'status' : 'FAILED' , 'error' : 'Requested User haven\'t activated his account.'})
        except User.DoesNotExist :
            return Response({'status' : 'FAILED' , 'error' : 'Requested User Doesn\'t Exists in our database.'})

        # Check whether this have sent a request already or not 
        try:
            status = UserFriends.objects.get(from_user = request.user, to_user = user)
            try : 
                opp_status = UserFriends.objects.get(from_user = user, to_user = request.user)
                opp_status.delete()
            except UserFriends.DoesNotExist :
                its_ok = True
            status.delete()
            return Response({'status' : 'OK' , 'result' : 'Removed Successfully!'})
        except UserFriends.DoesNotExist:
            try : 
                opp_status = UserFriends.objects.get(from_user = user, to_user = request.user)
                opp_status.delete()
                return Response({'status' : 'OK' , 'result' : 'Removed Successfully!'})
            except UserFriends.DoesNotExist :
                return Response({'status' : 'FAILED' , 'error' : 'Already Deleted!'})

class AcceptFriendRequest(generics.GenericAPIView):

    serializer_class = AcceptFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):

        if Profile.objects.get(owner = request.user).codeforces == "" or Profile.objects.get(owner = request.user).codeforces == None :
            return Response({'status': 'FAILED', 'error' : 'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '})

        from_user = request.data["from_user"]

        # Check this username is Valid or Not 
        try: 
            from_user = User.objects.get(username = from_user , is_verified = True)
            if Profile.objects.get(owner = from_user).codeforces == "" or Profile.objects.get(owner = from_user).codeforces == None :
                return Response({'status' : 'FAILED' , 'error' : 'Requested User haven\'t activated his account.'})
        except User.DoesNotExist :
            return Response({'status' : 'FAILED' , 'error' : 'Requested User Doesn\'t Exists in our database.'})

        # Check whether this have sent a request already or not 
        try:
            status = UserFriends.objects.get(from_user = from_user, to_user = request.user)
            if status.status :
                return Response({'status' : 'FAILED' , 'error' : 'You are already Friends!'})
            status.status = True
            status.save()
            return Response({'status' : 'OK' , 'result' : 'You are now Friends!'})
        except UserFriends.DoesNotExist:
            return Response({'status' : 'FAILED' , 'error' : 'No Request Found! It seems User have removed Request.'})

class FriendsShowView(generics.GenericAPIView):

    serializer_class = FriendsShowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self , request):

        if Profile.objects.get(owner = request.user).codeforces == "" or Profile.objects.get(owner = request.user).codeforces == None :
            return Response({'status': 'FAILED', 'error' : 'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '})

        friendsbyrequest = UserFriends.objects.filter(status = True , from_user = request.user)
        friendsbyaccept  = UserFriends.objects.filter(status = True , to_user = request.user)

        friendsbyrequest = FriendsShowSerializer(friendsbyrequest , context = {'by_to_user':True} , many = True).data
        friendsbyaccept = FriendsShowSerializer(friendsbyaccept , context = {'by_to_user':False} , many = True).data

        friends = friendsbyrequest + friendsbyaccept
        return Response({'status' : 'OK' , 'result' : friends})

class FriendRequestShowView(generics.GenericAPIView):

    serializer_class = FriendsShowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self , request):

        if Profile.objects.get(owner = request.user).codeforces == "" or Profile.objects.get(owner = request.user).codeforces == None :
            return Response({'status': 'FAILED', 'error' : 'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '})

        friendsbyaccept  = UserFriends.objects.filter(status = False , to_user = request.user)
        friendsbyaccept = FriendsShowSerializer(friendsbyaccept , context = {'by_to_user':False} , many = True).data
        return Response({'status' : 'OK' , 'result' : friendsbyaccept})

class RequestSendShowView(generics.GenericAPIView):

    serializer_class = FriendsShowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self , request):

        if Profile.objects.get(owner = request.user).codeforces == "" or Profile.objects.get(owner = request.user).codeforces == None :
            return Response({'status': 'FAILED', 'error' : 'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '})

        friendsbyrequest = UserFriends.objects.filter(status = False , from_user = request.user)
        friendsbyrequest = FriendsShowSerializer(friendsbyrequest , context = {'by_to_user':True} , many = True).data
        return Response({'status' : 'OK' , 'result' : friendsbyrequest})


# Friends Related View Ends
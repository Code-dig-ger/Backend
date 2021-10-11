from django.shortcuts import render
from rest_framework import generics, status, permissions, views
from .serializers import (
    RegisterSerializer, ProfileSerializer, EmailVerificationSerializer,
    LoginSerializer, RequestPasswordResetEmailSeriliazer,
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer,
    SendEmailVerificationSerializer, PasswordChangeSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile
from lists.models import Solved
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt, json
from .permissions import *
from rest_framework.generics import RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import UpdateAPIView, ListAPIView, ListCreateAPIView
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
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Validations
from .param_validators import isValidRequest
# Return Response
from .response import response
from .exception import ValidationException
# Profile
from .profile import ( get_atcoder_profile, get_spoj_profile, 
                        get_uva_profile, get_codechef_profile, 
                        get_codeforces_profile )
from codeforces.models import user as CodeforcesUser
from codeforces.models import user_contest_rank
from codeforces.serializers import UserSerializer as CodeforcesUserSerializer
from django.db.models import Q
from lists.models import Solved

# Friends
from .serializers import ( SendFriendRequestSerializer, RemoveFriendSerializer, 
                            AcceptFriendRequestSerializer, FriendsShowSerializer )
from .models import UserFriends


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Endpoint for registering a user 
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        relative_link = reverse('email-verify')
        redirect_url = request.GET.get('redirect_url', None)
        absurl = 'https://' + current_site + relative_link + "?token=" + str(
            token)
        if redirect_url != None:
            absurl += "&redirect_url=" + redirect_url
        email_body = {}
        email_body['username'] = user.username
        email_body['message'] = 'Verify your email'
        email_body['link'] = absurl
        data = {
            'email_body': email_body,
            'email_subject': 'Codedigger - Email Confirmation',
            'to_email': user.email
        }
        Util.send_email(data)
        return response(user_data, Status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token',
                                           in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        """
        Endpoint for verification of the mail
        """
        token = request.GET.get('token')
        redirect_url = request.GET.get('redirect_url', None)
        if redirect_url is None:
            redirect_url = os.getenv('EMAIL_REDIRECT')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return redirect(redirect_url + '?email=SuccessfullyActivated')
        except jwt.ExpiredSignatureError as identifier:
            return redirect(redirect_url + '?email=ActivationLinkExpired')
        except jwt.exceptions.DecodeError as identifier:
            return redirect(redirect_url + '?email=InvalidToken')


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Endpoint for logging in a user
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'current_site': get_current_site(request).domain})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckAuthView(views.APIView):
    permission_classes = [Authenticated]

    def get(self, request, *args, **kwargs):
        """
        Endpoint for checking if user is authenticated or not by checking if the JWT token is valid or not.
        """
        return response(Data="Token is Valid")


class SendVerificationMail(generics.GenericAPIView):
    serializer_class = SendEmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        """
        Endpoint for sending a verification mail
        """
        email = request.data.get('email', None)
        if email is None:
            raise ValidationException('Email not provided')
        if not User.objects.filter(email=email).exists():
            raise ValidationException('The given email does not exist')
        user = User.objects.get(email=email)
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        redirect_url = request.GET.get('redirect_url', None)
        absurl = 'https://' + current_site + relative_link + "?token=" + str(
            token)
        if redirect_url != None:
            absurl += "&redirect_url=" + redirect_url
        email_body = {}
        email_body['username'] = user.username
        email_body['message'] = 'Verify your email'
        email_body['link'] = absurl
        data = {
            'email_body': email_body,
            'email_subject': 'Codedigger - Email Verification',
            'to_email': user.email
        }
        Util.send_email(data)
        return response(Data="A Verification Email has been sent")


class ProfileGetView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [Authenticated, IsOwner]
    queryset = Profile.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [Authenticated, IsOwner]
    queryset = Profile.objects.all()
    lookup_field = "owner_id__username"

    def get_serializer_context(self, **kwargs):
        data = super().get_serializer_context(**kwargs)
        data['user'] = self.request.user.username
        return data

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_update(self, serializer):
        uva = self.request.data.get('uva_handle', None)
        if uva == None:
            return serializer.save()
        ele = get_uva(uva)
        if int(ele) > 0:
            return serializer.save(uva_id=ele)
        else:
            return serializer.save()


class ChangePassword(generics.GenericAPIView):
    permission_classes = [Authenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        """
        Endpoint for changing the password
        """
        data = request.data
        old_pass = data.get('old_pass', None)
        new_pass = data.get('new_pass', None)
        if old_pass is None or new_pass is None:
            raise ValidationException(
                'Either the old or new password was not provided')
        user = authenticate(username=self.request.user.username,
                            password=old_pass)
        if new_pass == old_pass:
            raise ValidationException(
                "The new password is same as the old password")
        if len(new_pass) < 6:
            raise ValidationException(
                "The password is too short, should be of minimum length 6")
        if user is None:
            raise ValidationException("Wrong Password")
        user.set_password(new_pass)
        user.save()
        return response(Data="Password Change Complete")


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        """
        Endpoint for sending the password reset email
        """
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', None)
        if email is None:
            raise ValidationException('Email has not been provided')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.auth_provider != 'email':
                raise ValidationException(
                    'You cannot reset password if you registered with google')
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm',
                                   kwargs={
                                       'uidb64': uidb64,
                                       'token': token
                                   })

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'https://' + current_site + relativeLink
            email_body = {}
            email_body['username'] = user.username
            email_body['message'] = 'Reset your Password'
            email_body['link'] = absurl + "?redirect_url=" + redirect_url
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Codedigger - Password Reset'
            }
            Util.send_email(data)
            return response(
                Data="We have sent you a link to reset your password")
        raise ValidationException('The given email does not exist')


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        """
        Endpoint which verifies the token used for resetting the password
        """
        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            if not User.objects.filter(id=id).exists():
                raise ValidationException("UIDB Token is invalid")
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if redirect_url and len(redirect_url) > 3:
                    return redirect(redirect_url + '?token_valid=False')
                else:
                    return redirect(
                        os.getenv('FRONTEND_URL', '') + '?token_valid=False')
            if redirect_url and len(redirect_url) > 3:
                return redirect(
                    redirect_url +
                    '?token_valid=True&message=Credentials Valid&uidb64=' +
                    uidb64 + '&token=' + token)
            else:
                return redirect(
                    os.getenv('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return redirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                raise ValidationException(
                    'Token is not valid, please request a new one')
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationException(
                    'Token is invalid. Please request a new one')


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """
        Endpoint for changing the password in the profile
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response(Data="Password reset success")


class SearchUser(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AuthenticatedOrReadOnly]

    def get(self, request):

        search = request.GET.get('q')

        profiles = Profile.objects.filter(owner__is_verified=True).exclude(
            name=None).exclude(codeforces=None)

        if search != None:
            q = Q()
            q |= Q(owner__username__icontains=search)
            q |= Q(codeforces__icontains=search)
            q |= Q(codechef__icontains=search)
            q |= Q(uva_handle__icontains=search)
            q |= Q(atcoder__icontains=search)
            q |= Q(name__icontains=search)
            q |= Q(spoj__icontains=search)
            profiles = profiles.filter(q)

        profiles = profiles.order_by('?')[:20]

        #TODO Exclude friends in search not-important

        search_data = []
        for profile in profiles:
            data = ProfileSerializer(profile).data
            data['username'] = profile.owner.username
            data['email'] = profile.owner.email
            username = profile.owner.username
            if request.user.is_authenticated:
                if request.user.username == username:
                    data['about_user'] = 'Logged In User Itself'
                    data['about_mentor'] = 'Logged In User Itself'
                else:
                    # Check for friends
                    if UserFriends.objects.filter(
                            status=True,
                            to_user=request.user,
                            from_user=User.objects.get(
                                username=username)).exists():
                        data['about_user'] = 'Friends'
                    elif UserFriends.objects.filter(
                            status=True,
                            to_user=User.objects.get(username=username),
                            from_user=request.user).exists():
                        data['about_user'] = 'Friends'
                    elif UserFriends.objects.filter(
                            status=False,
                            to_user=User.objects.get(username=username),
                            from_user=request.user).exists():
                        data['about_user'] = 'Request Sent'
                    elif UserFriends.objects.filter(
                            status=False,
                            to_user=request.user,
                            from_user=User.objects.get(
                                username=username)).exists():
                        data['about_user'] = 'Request Received'
                    else:
                        data['about_user'] = 'Stalking'

                    data['about_mentor'] = 'Not Mentor'
                    for mentor in Profile.objects.get(
                            owner=request.user).gurus.split(','):
                        if mentor.casefold() == data['codeforces'].casefold():
                            data['about_mentor'] = 'Mentor'
                            break
            else:
                data['about_user'] = 'Not Authenticated'
                data['about_mentor'] = 'Not Authenticated'

            search_data.append(data)

        return Response({'status': 'OK', 'result': search_data})


# Profile View


class UserProfileGetView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AuthenticatedOrReadOnly]

    def get(self, request, username):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationException(
                'Requested User doesn\'t exists in our database. Register Now! :)'
            )

        profile = Profile.objects.get(owner=user)

        if profile.codeforces == None:
            raise ValidationException(
                'Requested User haven\'t activated his/her account. :( ')

        ermsg = "You haven\'t entered {} handle in your Profile. Update Profile Now! "

        data = {}

        if request.GET.get('platform') == None:
            # Send Profile
            data = ProfileSerializer(profile).data
            data['username'] = user.username
            data['email'] = user.email
            if request.user.is_authenticated:
                if request.user.username == username:
                    data['about_user'] = 'Logged In User Itself'
                    data['about_mentor'] = 'Logged In User Itself'
                else:
                    # Check for friends
                    if UserFriends.objects.filter(
                            status=True,
                            to_user=request.user,
                            from_user=User.objects.get(
                                username=username)).exists():
                        data['about_user'] = 'Friends'
                    elif UserFriends.objects.filter(
                            status=True,
                            to_user=User.objects.get(username=username),
                            from_user=request.user).exists():
                        data['about_user'] = 'Friends'
                    elif UserFriends.objects.filter(
                            status=False,
                            to_user=User.objects.get(username=username),
                            from_user=request.user).exists():
                        data['about_user'] = 'Request Sent'
                    elif UserFriends.objects.filter(
                            status=False,
                            to_user=request.user,
                            from_user=User.objects.get(
                                username=username)).exists():
                        data['about_user'] = 'Request Received'
                    else:
                        data['about_user'] = 'Stalking'

                    data['about_mentor'] = 'Not Mentor'
                    for mentor in Profile.objects.get(
                            owner=request.user).gurus.split(','):
                        if mentor.casefold() == data['codeforces'].casefold():
                            data['about_mentor'] = 'Mentor'
                            break
            else:
                data['about_user'] = 'Not Authenticated'
                data['about_mentor'] = 'Not Authenticated'

        elif request.GET.get('platform') == "codeforces":

            try:
                codeforces_user = CodeforcesUser.objects.get(
                    handle=profile.codeforces)
            except CodeforcesUser.DoesNotExist:
                codeforces_user = None

            codeforces_user, codeforces_data = get_codeforces_profile(
                profile.codeforces, codeforces_user)
            if codeforces_user != None:
                data = CodeforcesUserSerializer(codeforces_user).data
                data['status'] = codeforces_data['status']
                data['contribution'] = codeforces_data['contribution']
                data['avatar'] = codeforces_data['avatar']
                data['lastOnlineTimeSeconds'] = codeforces_data[
                    'lastOnlineTimeSeconds']
                data['friendOfCount'] = codeforces_data['friendOfCount']
            else:
                data = codeforces_data

            data['solvedCount'] = Solved.objects.filter(
                user=profile.owner, problem__platform='C').count()

        elif request.GET.get('platform') == "codechef":
            if profile.codechef != "" and profile.codechef != None:
                data = get_codechef_profile(profile.codechef)
            else:
                raise ValidationException(ermsg.format('codechef'))

        elif request.GET.get('platform') == "atcoder":
            if profile.atcoder != "" and profile.atcoder != None:
                data = get_atcoder_profile(profile.atcoder)
                data['solvedCount'] = Solved.objects.filter(
                    user=profile.owner, problem__platform='A').count()
            else:
                raise ValidationException(ermsg.format('atcoder'))

        elif request.GET.get('platform') == "uva":
            if profile.uva_handle != "" and profile.uva_handle != None:
                data = get_uva_profile(profile.uva_id, profile.uva_handle)
            else:
                raise ValidationException(ermsg.format('uva'))

        elif request.GET.get('platform') == "spoj":
            if profile.spoj != "" and profile.spoj != None:
                data = get_spoj_profile(profile.spoj)
            else:
                raise ValidationException(ermsg.format('spoj'))
        else:
            raise ValidationException('Invalid GET Request')

        return response(Data=data)


# Friends Related View Start


class SendFriendRequest(generics.GenericAPIView):

    serializer_class = SendFriendRequestSerializer
    permission_classes = [AuthenticatedActivated]

    def post(self, request):

        to_user = request.data["to_user"]

        # Check this username is Valid or Not

        if Profile.objects.get(
                owner=request.user).codeforces == "" or Profile.objects.get(
                    owner=request.user).codeforces == None:
            raise ValidationException(
                'You have not activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '
            )

        if request.user.username == to_user:
            raise ValidationException(
                'You cannot send a friend request to yourself.')

        try:
            to_user = User.objects.get(username=to_user, is_verified=True)
            if Profile.objects.get(
                    owner=to_user).codeforces == "" or Profile.objects.get(
                        owner=to_user).codeforces == None:
                raise ValidationException(
                    'Requested User have not activated his account.')
        except User.DoesNotExist:
            raise ValidationException(
                'Requested User Does not Exists in our database.')

        # Check whether this have sent a request already or not
        try:
            uf = UserFriends.objects.get(from_user=request.user,
                                         to_user=to_user)
            if uf.status == True:
                raise ValidationException('You are already Friends.')
            else:
                raise ValidationException(
                    'You have already Sent a Friend Request to this User.')
        except UserFriends.DoesNotExist:
            # Check for Opposite

            try:
                uf = UserFriends.objects.get(from_user=to_user,
                                             to_user=request.user)
                if uf.status == True:
                    raise ValidationException('You are already Friends.')
                else:
                    status.status = True
                    return response(Data="You are now Friends")

            except UserFriends.DoesNotExist:
                UserFriends.objects.create(from_user=request.user,
                                           to_user=to_user,
                                           status=False)
                return response(Data="Friend Request Sent")


class RemoveFriend(generics.GenericAPIView):

    serializer_class = RemoveFriendSerializer
    permission_classes = [AuthenticatedActivated]

    def post(self, request):

        if Profile.objects.get(
                owner=request.user).codeforces == "" or Profile.objects.get(
                    owner=request.user).codeforces == None:
            raise ValidationException(
                'You have not activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '
            )

        user = request.data["user"]

        # Check this username is Valid or Not
        try:
            user = User.objects.get(username=user, is_verified=True)
            if Profile.objects.get(
                    owner=user).codeforces == "" or Profile.objects.get(
                        owner=user).codeforces == None:
                raise ValidationException(
                    'Requested User haven\'t activated his account.')
        except User.DoesNotExist:
            raise ValidationException(
                'Requested User Doesn\'t Exists in our database.')

        # Check whether this have sent a request already or not
        try:
            uf = UserFriends.objects.get(from_user=request.user, to_user=user)
            try:
                opp_status = UserFriends.objects.get(from_user=user,
                                                     to_user=request.user)
                opp_status.delete()
            except UserFriends.DoesNotExist:
                its_ok = True
            uf.delete()
            return response(Data="Removed Successfully!")
        except UserFriends.DoesNotExist:
            try:
                opp_status = UserFriends.objects.get(from_user=user,
                                                     to_user=request.user)
                opp_status.delete()
                return response(Data="Removed Successfully!")
            except UserFriends.DoesNotExist:
                raise ValidationException('Already Deleted!')


class AcceptFriendRequest(generics.GenericAPIView):

    serializer_class = AcceptFriendRequestSerializer
    permission_classes = [AuthenticatedActivated]

    def put(self, request):

        if Profile.objects.get(
                owner=request.user).codeforces == "" or Profile.objects.get(
                    owner=request.user).codeforces == None:
            raise ValidationException(
                'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '
            )

        from_user = request.data["from_user"]

        # Check this username is Valid or Not
        try:
            from_user = User.objects.get(username=from_user, is_verified=True)
            if Profile.objects.get(
                    owner=from_user).codeforces == "" or Profile.objects.get(
                        owner=from_user).codeforces == None:
                raise ValidationException(
                    'Requested User haven\'t activated his account.')
        except User.DoesNotExist:
            raise ValidationException(
                'Requested User Doesn\'t Exists in our database.')

        # Check whether this have sent a request already or not
        try:
            uf = UserFriends.objects.get(from_user=from_user,
                                         to_user=request.user)
            if uf.status:
                raise ValidationException('You are already Friends!')
            uf.status = True
            uf.save()
            return Response({'status': 'OK', 'result': 'You are now Friends!'})
        except UserFriends.DoesNotExist:
            raise ValidationException(
                'No Request Found! It seems User have removed Request.')


class FriendsShowView(generics.GenericAPIView):

    serializer_class = FriendsShowSerializer
    permission_classes = [AuthenticatedActivated]

    def get(self, request):

        if Profile.objects.get(
                owner=request.user).codeforces == "" or Profile.objects.get(
                    owner=request.user).codeforces == None:
            raise ValidationException(
                'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '
            )

        friendsbyrequest = UserFriends.objects.filter(status=True,
                                                      from_user=request.user)
        friendsbyaccept = UserFriends.objects.filter(status=True,
                                                     to_user=request.user)

        friendsbyrequest = FriendsShowSerializer(friendsbyrequest,
                                                 context={
                                                     'by_to_user': True
                                                 },
                                                 many=True).data
        friendsbyaccept = FriendsShowSerializer(friendsbyaccept,
                                                context={
                                                    'by_to_user': False
                                                },
                                                many=True).data

        friends = friendsbyrequest + friendsbyaccept
        return response(Data=friends)


class FriendRequestShowView(generics.GenericAPIView):

    serializer_class = FriendsShowSerializer
    permission_classes = [AuthenticatedActivated]

    def get(self, request):

        if Profile.objects.get(
                owner=request.user).codeforces == "" or Profile.objects.get(
                    owner=request.user).codeforces == None:
            raise ValidationException(
                'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '
            )

        friendsbyaccept = UserFriends.objects.filter(status=False,
                                                     to_user=request.user)
        friendsbyaccept = FriendsShowSerializer(friendsbyaccept,
                                                context={
                                                    'by_to_user': False
                                                },
                                                many=True).data
        return response(Data=friendsbyaccept)


class RequestSendShowView(generics.GenericAPIView):

    serializer_class = FriendsShowSerializer
    permission_classes = [AuthenticatedActivated]

    def get(self, request):

        if Profile.objects.get(
                owner=request.user).codeforces == "" or Profile.objects.get(
                    owner=request.user).codeforces == None:
            raise ValidationException(
                'You have\'n activated your account. Please activate your account by putting your name and codeforces handle in your profile.. '
            )

        friendsbyrequest = UserFriends.objects.filter(status=False,
                                                      from_user=request.user)
        friendsbyrequest = FriendsShowSerializer(friendsbyrequest,
                                                 context={
                                                     'by_to_user': True
                                                 },
                                                 many=True).data
        return response(Data=friendsbyrequest)


# Friends Related View Ends

from django.template.loader import render_to_string
from django.http import HttpResponse


def testing(request):

    context = {
        'username': 'shivamsinghal1012',
        'message': 'Verify your Email ',
        'link': 'https://google.com'
    }

    return HttpResponse(render_to_string('user/send_mail.html', context))

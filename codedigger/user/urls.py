from django.urls import path
from .views import (
     RegisterView,
     VerifyEmail,
     LoginApiView,
     ProfileGetView,
     ProfileUpdateView,
     PasswordTokenCheckAPI,
     RequestPasswordResetEmail,
     SetNewPasswordAPIView,
     UserProfileGetView,
     ChangePassword,
     SendVerificationMail,
     CheckAuthView
)
# Friend Related View
from .views import SendFriendRequest, RemoveFriend, AcceptFriendRequest, FriendsShowView
from .views import FriendRequestShowView, RequestSendShowView

from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/',RegisterView.as_view(),name = "register"),
    path('email-verify/',VerifyEmail.as_view(),name = "email-verify"),
    path('send-email/',SendVerificationMail.as_view(),name='send-email'),
    path('profile/',ProfileGetView.as_view(),name = "profile"),
    path('profile/<str:owner_id__username>',ProfileUpdateView.as_view(),name = "profile"),
    path('profile/<str:username>/',UserProfileGetView.as_view(),name = "userProfile"),
    path('login/',LoginApiView.as_view(),name = "login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'), 
    path('password-change/',ChangePassword.as_view(),name='password-change'),
    path('check-auth/',CheckAuthView.as_view(),name='check-auth'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),

    # Friends Related Path Start
    path('user/send-request' , SendFriendRequest.as_view() , name='Send_Friend_Request'),
    path('user/remove-friend' , RemoveFriend.as_view() , name='Remove_Friend'),
    path('user/accept-request' , AcceptFriendRequest.as_view() , name='Accept_Friend_Request'),
    path('user/friends' , FriendsShowView.as_view() , name='Show_Friends_List'),
    path('user/show-request' , FriendRequestShowView.as_view() , name='Show_Friend_Request_List'),
    path('user/show-send-request' , RequestSendShowView.as_view() , name='Show_Friend_Request_Send_List'),

    # Friends Related Path End
]

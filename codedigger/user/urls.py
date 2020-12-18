from django.urls import path
from .views import RegisterView,VerifyEmail,LoginApiView,ProfileGetView,ProfileUpdateView,PasswordTokenCheckAPI, RequestPasswordResetEmail,SetNewPasswordAPIView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/',RegisterView.as_view(),name = "register"),
    path('email-verify/',VerifyEmail.as_view(),name = "email-verify"),
    path('profile/',ProfileGetView.as_view(),name = "profile"),
    path('profile/<str:owner_id__username>',ProfileUpdateView.as_view(),name = "profile"),
    path('login/',LoginApiView.as_view(),name = "login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]

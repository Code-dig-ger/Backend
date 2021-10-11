from rest_framework import generics

from user.response import response
from user.exception import ValidationException

from .permissions import AuthenticatedBot
from .serializers import VerifySerializer
from .utils import get_user, get_user_profile


class VerifyView(generics.GenericAPIView):
    
    permission_classes = [AuthenticatedBot]
    serializer_class = VerifySerializer
    

    def put(self, request):
        """
            username: username of user to be verify 
            discord_tag: discord tag to be checked

            Verify if the provided discord_tag is equal to 
            provided in profile of user 
        """
        username = request.data.get('username', None)
        discord_tag = request.data.get('discord_tag', None)

        user = get_user(username)
        profile = get_user_profile(user)

        if profile.discord_tag == discord_tag:
            profile.is_discord_verified = True
            profile.save()
        else:
            raise ValidationException(
                'Discord Tag not matched with your profile. Please login to https://codedigger.tech and update your profile.'
            )
        
        return response('Thanks for verifying!')
from rest_framework import serializers

from user.models import Profile


class VerifySerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100)
    discord_tag = serializers.CharField(max_length=64)

    class Meta:
        model = Profile
        fields = [
            'username',
            'discord_tag'
        ]
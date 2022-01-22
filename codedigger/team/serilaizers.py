from rest_framework import serializers
from .models import Team
import string,random,datetime
from django.db import models
class TeamSerializers(serializers.ModelSerializer):
#    user=User.
    def create(self, validated_data):
        return Team.objects.create(
            name=validated_data['Team_name'],
            created_at=datetime.date.today(),
            Invitation_code=''.join(random.choices(string.ascii_uppercase + string.digits+string.ascii_lowercase, k = 10))    
            )
        # team_object.save()
    class Meta:
        model=Team
        feilds=['Team_name']
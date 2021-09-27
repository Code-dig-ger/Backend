from rest_framework import serializers
from .models import CodeforcesContest, CodeforcesContestSubmission, CodeforcesContestParticipation
from codeforces.serializers import MiniUserSerializer


class CodeforcesContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeforcesContest
        fields = [
            'name', 'contestId', 'groupId', 'Type', 'nproblems',
            'showOnlyOfficial'
        ]


class CodeforcesContestSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeforcesContestSubmission
        fields = [
            'problemIndex', 'submissionId', 'isSolved', 'penalty', 'lang'
        ]


class CodeforcesContestParticipationSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer()
    submissions = serializers.SerializerMethodField()

    def get_submissions(self, obj):
        qs = CodeforcesContestSubmission.objects.filter(participant=obj)
        return CodeforcesContestSubmissionSerializer(qs, many=True).data

    class Meta:
        model = CodeforcesContestParticipation
        fields = [
            'participantId', 'isOfficial', 'isVirtual', 'user', 'submissions'
        ]

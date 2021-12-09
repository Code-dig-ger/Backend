from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CodeforcesContest)
admin.site.register(CodeforcesContestProblem)

# admin.site.register(Contest)
# admin.site.register(ContestProblem)
# admin.site.register(ContestParticipation)
# admin.site.register(ContestResult)
# admin.site.register(CodeforcesContest)
# admin.site.register(CodeforcesContestParticipation)
# admin.site.register(CodeforcesContestSubmission)
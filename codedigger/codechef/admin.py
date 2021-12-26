from django.contrib import admin
from .models import CodechefContest, CodechefContestProblems, User
# Register your models here.
admin.site.register(CodechefContest)
admin.site.register(CodechefContestProblems)
admin.site.register(User)

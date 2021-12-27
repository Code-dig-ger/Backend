from django.contrib import admin
from .models import List, ListInfo, Solved, ListExtraInfo, LadderStarted, Enrolled


class ListInfoAdmin(admin.ModelAdmin):
    search_fields = ('p_list__name', 'problem__name', 'problem__prob_id')


class ListAdmin(admin.ModelAdmin):
    search_fields = ('owner__username', 'name', 'type_list', 'public')


class SolvedAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'problem__prob_id', 'problem__name')


class ListExtraInfoAdmin(admin.ModelAdmin):
    search_fields = ('curr_list__name', )


class LadderStartedAdmin(admin.ModelAdmin):
    search_fields = ('ladder_user__name', 'user__username')


class EnrolledAdmin(admin.ModelAdmin):
    search_fields = ('enroll__user', 'enroll__list')


admin.site.register(List, ListAdmin)
admin.site.register(ListInfo, ListInfoAdmin)
admin.site.register(Solved, SolvedAdmin)
admin.site.register(ListExtraInfo, ListExtraInfoAdmin)
admin.site.register(LadderStarted, LadderStartedAdmin)
admin.site.register(Enrolled, EnrolledAdmin)

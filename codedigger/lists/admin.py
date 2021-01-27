from django.contrib import admin
from .models import List,ListInfo,Solved,ListExtraInfo

class ListInfoAdmin(admin.ModelAdmin):
    search_fields = ('p_list__name','problem__name','problem__prob_id')

class ListAdmin(admin.ModelAdmin):
    search_fields = ('owner__username','name','type_list','public')

class SolvedAdmin(admin.ModelAdmin):
    search_fields = ('user__username','problem__prob_id','problem__name')

class ListExtraInfoAdmin(admin.ModelAdmin):
    search_fields = ('curr_list__name')

admin.site.register(List,ListAdmin)
admin.site.register(ListInfo,ListInfoAdmin)
admin.site.register(Solved,SolvedAdmin)
admin.site.register(ListExtraInfo,)
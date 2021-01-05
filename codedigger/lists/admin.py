from django.contrib import admin

# Register your models here.
from .models import List,ListInfo,Solved

admin.site.register(List)
admin.site.register(ListInfo)
admin.site.register(Solved)
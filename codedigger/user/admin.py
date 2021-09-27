from django.contrib import admin
from .models import User, Profile, UserFriends


class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'username',
        'email',
    )


class ProfileAdmin(admin.ModelAdmin):
    search_fields = (
        'owner__username',
        'name',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserFriends)

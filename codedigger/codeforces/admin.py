from django.contrib import admin

# Register your models here.
from .models import organization , country , user , contest , user_contest_rank , organization_contest_participation, country_contest_participation


admin.site.register(organization)
admin.site.register(country)
admin.site.register(user)
admin.site.register(contest)
admin.site.register(user_contest_rank)
admin.site.register(organization_contest_participation)
admin.site.register(country_contest_participation)


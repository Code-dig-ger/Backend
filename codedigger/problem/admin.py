from django.contrib import admin
from .models import Problem


class ProblemAdmin(admin.ModelAdmin):
    search_fields = (
        'prob_id',
        'platform',
        'name',
    )


admin.site.register(Problem, ProblemAdmin)

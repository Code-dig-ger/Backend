from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="CodeDigger API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('user.urls')),
    path('social_auth/', include(('social_auth.urls', 'social_auth'),namespace="social_auth")),
    path('problems/',include('problem.urls')),
    path('codeforces/',include('codeforces.urls')),
    path('lists/',include('lists.urls')),
    path('blog/' , include('blog.urls')),
    path('contest/' , include('contest.urls')),
    
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
]
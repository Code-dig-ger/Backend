from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CodeDigger API",
        default_version='v1',
        description=
        "This project aims at accumulating the data of competitive programming platforms into one platform - CodeDigger. We have used the Codeforces, Codechef, AtCoder, Spoj and UVA data in our project. We have used their publicly available APIs and introduced several features into out application such as friends, mentors, ladders and upsolve. This can be the ultimate stop for everyone practicing competitive programming. Users can login with email or google and check their rating and best contests in which they have performed on every site and look at the remaining questions in the contests given by them. We have also incorporated features such as ladders which will enable users to solve problems from different sites in a ladder-like fashion. They can also explore problems and filter them according to difficulty, rating topic, solved by friends or mentors, etc as per their needs.",
        terms_of_service="https://codedigger.tech/terms",
        contact=openapi.Contact(email="contact.codedigger@gmail.com"),
        license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('social_auth/',
         include(('social_auth.urls', 'social_auth'),
                 namespace="social_auth")),
    path('problems/', include('problem.urls')),
    path('codeforces/', include('codeforces.urls')),
    path('lists/', include('lists.urls')),
    path('blog/', include('blog.urls')),
    path('contest/', include('contest.urls')),
    path('',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

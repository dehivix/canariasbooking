from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

#Changing main system title
admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path(
        "home2",
        TemplateView.as_view(template_name="pages/home.html"),
        name="home2",
    ),

    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),

    # Django JET URLS
    path(
        'jet/',
        include('jet.urls', 'jet'),
    ),

    path(
        'jet/dashboard/',
        include('jet.dashboard.urls', 'jet-dashboard'),
    ),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # User management
    path(
        "users/",
        include("apps.users.urls", namespace="users"),
    ),

    path(
        "accounts/",
        include("allauth.urls"),
    ),

    path(
        "",
        include("apps.bookings.urls"),
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path(
        "api/",
        include("config.api_router"),
    ),

    # DRF auth token
    path(
        "auth-token/",
        obtain_auth_token,
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),

        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),

        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),

        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

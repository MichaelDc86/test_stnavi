"""snavi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/', include('project.api.urls', namespace='api')),
    re_path('', include('rest_auth.urls')),


    # re_path('^api/', include('authapp.api.urls', namespace='api')),
    # re_path('^message/', include('message.api.urls', namespace='message')),
    #
    # re_path('^', include('rest_auth.urls')),
    # re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', TemplateView.as_view(), name='password_reset_confirm'),
    #
    # re_path(r'^auth/verify/social/', include("social_django.urls", namespace="social")),
    # re_path(r'^social/', include('auth_social.urls', namespace='social_view')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

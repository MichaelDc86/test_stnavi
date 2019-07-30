import project.views as views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'project'

urlpatterns = [

    url(r'^users/$', views.ProjectUserList.as_view(), name='users-list'),
    url(r'^users/(?P<pk>\d+)/$', views.ProjectUserDetail.as_view(), name='users-detail'),
    url(r'^posts/$', views.PostsList.as_view(), name='posts-list'),
    url(r'^posts/(?P<pk>\d+)/$', views.PostsDetail.as_view(), name='posts-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])


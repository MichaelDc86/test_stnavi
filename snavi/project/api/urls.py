import project.views as views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from project.views import ProjectUserList

app_name = 'project'

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^users/$', ProjectUserList.as_view(), name='users-list'),
    url(r'^users/(?P<pk>\d+)/$', views.ProjectUserList.as_view(), name='users-detail'),
    url(r'^posts/$', views.PostsList.as_view(), name='posts-list'),

    # url(r'^projects/(?P<pk>\d+)/$', ProjectDetail.as_view(), name='project-detail'),
    # url(r'^stages/$', StageList.as_view(), name='stage-list'),
    # url(r'^stages/(?P<pk>\d+)/$', StageDetail.as_view(), name='stage-detail'),
    # url(r'^tasks/$', TaskList.as_view(), name='task-list'),
    # url(r'^tasks/(?P<pk>\d+)/$', TaskDetail.as_view(), name='task-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])


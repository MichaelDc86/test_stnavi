from django_filters.rest_framework import DjangoFilterBackend
from project.api.serializers import ProjectUserSerializer, PostSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from project.models import ProjectUser, Post


class CustomProjectsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


@api_view(['GET'])
def api_root(request):

    return Response({
        'users': reverse('api:users-list', request=request),
        'posts': reverse('api:posts-list', request=request),

    })


class ProjectUserList(generics.ListCreateAPIView):

    model = ProjectUser
    queryset = ProjectUser.objects.all()  # .order_by('is_active', 'username')
    serializer_class = ProjectUserSerializer
    pagination_class = CustomProjectsSetPagination
    # parser_classes = (MultiPartParser,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user_ptr_id',)


class PostsList(generics.ListCreateAPIView):

    model = Post
    queryset = Post.objects.all()  # .order_by('is_active', 'username')
    serializer_class = PostSerializer
    pagination_class = CustomProjectsSetPagination
    parser_classes = (MultiPartParser,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id__user',)

from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from project.api.serializers import ProjectUserSerializer, PostSerializer, PostUpdateSerializer
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions

from project.models import ProjectUser, Post

from rest_framework.permissions import IsAuthenticated


class CustomProjectsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


@api_view()  # by default ['GET']
def api_root(request):

    return Response({
        'users': reverse('api:users-list', request=request),
        'posts': reverse('api:posts-list', request=request),
        'register': reverse('register', request=request),
        'login': reverse('rest_login', request=request),
        'logout': reverse('rest_logout', request=request),

    })


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
class ProjectUserList(generics.ListCreateAPIView):

    model = ProjectUser

    def get_queryset(self):
        user = self.request.user
        return ProjectUser.objects.filter(username=user.username)  # all().order_by('is_active', 'username')

    # queryset = ProjectUser.objects.all().order_by('is_active', 'username')
    serializer_class = ProjectUserSerializer
    pagination_class = CustomProjectsSetPagination
    parser_classes = (MultiPartParser,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user_ptr_id',)


class Register(generics.ListCreateAPIView):
    model = ProjectUser
    serializer_class = ProjectUserSerializer
    queryset = []  # ProjectUser.objects.none()


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
class ProjectUserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = ProjectUser

    def get_queryset(self):
        user = self.request.user
        return ProjectUser.objects.filter(username=user.username)

    serializer_class = ProjectUserSerializer


class PostsList(generics.ListCreateAPIView):

    model = Post

    def get_permissions(self):
        if self.request.method == 'GET':
            perms = []
        else:
            perms = [IsAuthenticated]
        return [p() for p in perms]

    queryset = Post.objects.all().order_by('date_created', 'title')
    serializer_class = PostSerializer
    pagination_class = CustomProjectsSetPagination
    parser_classes = (MultiPartParser,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id__user',)


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Post

    def get_queryset(self):
        self.queryset = Post.objects.all()  # filter(user_id=user.id).order_by('title')
        return self.queryset

    def get_serializer_class(self):
        user = self.request.user
        item = self.request.data.get('user')
        if user == item:
            self.serializer_class = PostSerializer
        else:
            self.serializer_class = PostUpdateSerializer
        return self.serializer_class

    def get_permissions(self):
        user = self.request.user
        item = self.request.data.get('user')
        if user == item:
            perms = []
        else:
            perms = [api_view(['GET', 'PUT'])]
        return [p() for p in perms]


# class DeletePermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blacklisted

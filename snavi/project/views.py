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
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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


@authentication_classes((SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication))
@permission_classes((IsAuthenticated,))
class ProjectUserList(generics.ListCreateAPIView):

    http_method_names = ['get', 'head']
    model = ProjectUser

    def get_queryset(self):
        user = self.request.user
        return ProjectUser.objects.filter(username=user.username)

    serializer_class = ProjectUserSerializer
    pagination_class = CustomProjectsSetPagination
    parser_classes = (MultiPartParser,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user_ptr_id',)


class Register(generics.ListCreateAPIView):
    http_method_names = ['post', 'head']
    model = ProjectUser
    serializer_class = ProjectUserSerializer
    queryset = []  # ProjectUser.objects.none()


    # def post(self, request, *args, **kwargs):
    #     message = f'To verify your signup on {settings.DOMAI_NAME} click the link'
    #     from_email = settings.DOMAI_NAME
    #     subject =
    #     send_mail(subject, message, from_email, [self.email], fail_silently=False, **kwargs)
    #     return self.create(request, *args, **kwargs)


@authentication_classes((SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication))
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
    # parser_classes = (MultiPartParser,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id__user',)


@authentication_classes((SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication))
@permission_classes((IsAuthenticated,))
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'patch']
    model = Post

    def get_queryset(self):
        self.queryset = Post.objects.filter(id=self.kwargs['pk'])
        return self.queryset

    def check_author(self):
        user = self.request.user.id
        item = self.get_object().user_id
        return bool(user == item)

    def get_serializer_class(self):

        if self.check_author():
            self.serializer_class = PostSerializer
        else:
            self.serializer_class = PostUpdateSerializer
        return self.serializer_class

    def get_permissions(self):

        if self.queryset:

            if self.queryset[0].user_id == self.request.user.id:
                if 'delete' not in self.http_method_names:
                    self.http_method_names.append('delete')
                perms = []
            else:
                perms = [IsAuthenticated, DeletePermission]
                if 'delete' in self.http_method_names:
                    self.http_method_names.remove('delete')
            return [p() for p in perms]
        else:
            return []


class DeletePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['DELETE', 'OPTIONS']:
            return False
        return True

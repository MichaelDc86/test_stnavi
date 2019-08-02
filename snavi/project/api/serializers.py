from project.models import ProjectUser, Post
from rest_framework import serializers

from django.core.mail import send_mail

from snavi import settings


class ProjectUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:users-detail')

    def create(self, validated_data):
        print('****************************************************************')
        user = ProjectUser(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        print('---------------------------------------------------------------------------')
        link = settings.DOMAIN_NAME + 'accounts/login'
        subject = 'Email verification for django'
        message = f'To verify your email on {settings.DOMAIN_NAME} click the {link}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

        return user

    class Meta:
        model = ProjectUser
        # fields = '__all__'
        fields = (
            'url',
            'email',
            'password',
            'username',
        )


class PostSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='api:posts-detail')

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        fields['user'].queryset = ProjectUser.objects.filter(username=request.user.username)
        fields['user'].view_name = 'api:users-detail'

        # if request.user:

        return fields

    class Meta:
        model = Post
        fields = '__all__'
        # fields = (
        #     'url',
        #     'user',
        #     'title',
        #     'date_created',
        #     'content',
        #     'like',
        # )


class PostUpdateSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='api:posts-detail')

    def get_fields(self):
        fields = super().get_fields()
        # request = self.context['request']

        return fields

    class Meta:
        model = Post
        fields = ('url', 'like', 'title',)
        read_only_fields = ['title', 'url']

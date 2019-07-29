from project.models import ProjectUser, Post
from rest_framework import serializers


class ProjectUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = ProjectUser(
            # email=validated_data['email'],
            username=validated_data['username'],
            # name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = ProjectUser
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(many=False, queryset=ProjectUser.objects.all())

    class Meta:
        model = Post
        fields = '__all__'

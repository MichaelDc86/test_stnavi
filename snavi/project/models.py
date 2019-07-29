import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProjectUser(User):

    image = models.ImageField(verbose_name='avatar', upload_to='projects_images', blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):

    user = models.ForeignKey(ProjectUser, verbose_name='author', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='title', max_length=128)
    date_created = models.DateField(verbose_name='creation date', default=datetime.date.today())
    content = models.CharField(verbose_name='content', max_length=512)
    like = models.BooleanField(verbose_name='like/unlike', default=False)

    def __str__(self):
        return self.title

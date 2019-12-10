from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from django.urls import reverse



# Create your models here.
#SQL modeli
class Post(models.Model):

    title = models.CharField(max_length=100)

    summary = models.TextField(max_length=200, default='Super recept! Usudi se probati...')

    content = models.TextField()

    image = models.ImageField(default='media\post_pics\default.jpg')

    date_posted = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):

        return self.title



    def get_absolute_url(self):

        return reverse('post-detail', kwargs={'pk': self.pk})

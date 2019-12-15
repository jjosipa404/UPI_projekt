from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from django.urls import reverse
from PIL import Image



# Create your models here.

#SQL modeli
class Post(models.Model):

    naslov = models.CharField(max_length=100)

    sazetak = models.TextField(max_length=200, default='Super recept! Usudi se probati...')

    sadrzaj = models.TextField()

    slika = models.ImageField(default='default.png', upload_to='post_pics')

    date_posted = models.DateTimeField(default=timezone.now)

    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.slika.path)
        img.save(self.slika.path)

    def __str__(self):
        return self.naslov



    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

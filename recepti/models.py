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

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        
    def approved(self):
        self.approved = True
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Komentar korisnika {}: {}'.format(self.user, self.content)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
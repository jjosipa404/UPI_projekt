from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from PIL import Image
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



# Create your models here.
 
#SQL modeli
class Post(models.Model):

    kategorije = [
        ('pr','predjelo'),
        ('gl','glavno jelo'),
        ('de','desert'),
    ]

    naslov = models.CharField(max_length=100)
    sazetak = models.TextField(max_length=200, default='Super recept! Usudi se probati...')
    sadrzaj = models.TextField()
    slika = models.ImageField(default='default_pict.jpg', upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    kategorija = models.CharField(max_length=2, choices=kategorije, default = 'gl')
    votes = GenericRelation(LikeDislike, related_query_name='posts')
    #like_count= models.IntegerField(default=0)
    #dislikes= models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.naslov

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.slika.path)

        if img.height > 640 or img.width > 320:
            output_size = (640, 320)
            img.thumbnail(output_size)
            img.save(self.slika.path)
        else:
            output_size = (640, 320)
            img.thumbnail(output_size)
            img.save(self.slika.path)


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name=_("Vote"), choices=VOTES)
    user = models.ForeignKey(User,verbose_name=_("User"), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
    
    def posts(self):
        return self.get_queryset().filter(content_type__model='post').order_by('-posts__date_posted')
    
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__created')

    def likes(self):
        #we take the queryset with record greater than 0
        return self.get_queryset().filter(vote__gt=0)
    
    def dislikes(self):
        #we take the queryset with records less than 0
        return self.get_queryset().filter(vote_lt=0)
    
    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    votes = GenericRelation(LikeDislike, related_query_name='comments')
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

#class Like(models.Model):
 #   post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
  #  user = models.ForeignKey(User, on_delete=models.CASCADE)
   # created = models.DateTimeField(auto_now_add=True)

'''
class Preference(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, related_name='preference', on_delete=models.CASCADE)
    value= models.PositiveIntegerField()
    date= models.DateTimeField(auto_now= True)

    
    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")
'''

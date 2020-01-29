from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from recepti.models import Post, Comment 
from users.models import Profile
from PIL import Image
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your tests here.

#----------------models tests---------------------------------------------------------------------
class PostTest(TestCase):
 
    def setUp(self):
        self.user = User.objects.create(username="user",password="password")
        
    
    def test_post_creation(self):
        post = Post.objects.create(naslov="test naslov", sazetak="test sazetak", sadrzaj="test sadrzaj",date_posted=timezone.now(),autor=self.user)
        self.assertTrue(isinstance(post, Post))
        self.assertEqual(post.__str__(), post.naslov)
   

    def test_get_absolute_url(self):
        post = Post.objects.create(naslov="test naslov", sazetak="test sazetak", sadrzaj="test sadrzaj",date_posted=timezone.now(),autor=self.user)
        self.assertEquals(post.get_absolute_url(),'/post/'+ str(post.pk) +'/')

   
class CommentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.post = Post.objects.create(naslov="test naslov", sazetak="test sazetak", sadrzaj="test sadrzaj",date_posted=timezone.now(),autor=self.user)
        self.comment = Comment.objects.create(post=self.post, user=self.user,content="test sadrzaj komentara",created=timezone.now())

        
    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment,Comment))
        self.assertEqual(self.comment.__str__(), 'Komentar korisnika ' + self.comment.user.username + ': '+ self.comment.content)


    def test_get_absolute_url(self):
        self.assertEquals(self.comment.get_absolute_url(),'/post/'+ str(self.post.pk) +'/')


class PostListViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('recepti-home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recepti-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recepti/home.html')

class UserPostListViewTest(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user',password='password')
        user1.save()


    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='user', password='password')
        response = self.client.get(reverse('user-posts',kwargs={'username': 'user'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recepti/user_posts.html')

class PostCreateViewTest(TestCase):

    def setUp(self):
        user = User.objects.create(username='user',password='password')
        user.save()
        post = Post.objects.create(naslov="test naslov", sazetak="test sazetak", sadrzaj="test sadrzaj",date_posted=timezone.now(),autor=user)
        post.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post-create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    #def test_logged_in(self):
       # login = self.client.login(username='user', password='password')
    #    response = self.client.get(reverse('post-create'))
   #     self.assertEqual(response.status_code, 200)


    
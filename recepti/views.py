import json
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (

    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView

)

from .models import Post, Comment 
from .filters import PostFilter

def home(request):
    postovi=Post.objects.all()
    search=request.GET('search')
    if search !='' and search is not None:
        postovi=postovi.Postfilter(naslov__icontains=search)

        context={
            'posts': postovi
        }
    else:
    
        context = {
            'posts': Post.objects.all()
        }
    return render(request, 'recepti/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'recepti/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'recepti/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'

    paginate_by = 12

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(autor=user).order_by('-date_posted')

class UserFavoriteListView(ListView):
    model = Post
    template_name = 'recepti/category_favorite.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    success_url = '/'

    paginate_by = 12

    def get_queryset(self):
        posts = Post.objects.all()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked_posts = []
        for post in posts:
            ids = post.votes.user_ids()
            for id,time in ids:
                if id == user.id:
                    liked_posts.append(post)
        return liked_posts

class CategoryPredjeloListView(ListView):
    model = Post
    template_name = 'recepti/category_predjelo.html'
    context_object_name = 'category-predjelo'
    paginate_by = 12
    

    def get_context_data(self, **kwargs):
        context = {
            'posts': Post.objects.all()
        }
        return context

class CategoryGlavnoListView(ListView):
    model = Post
    template_name = 'recepti/category_glavno.html'
    context_object_name = 'category-glavno'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = {
            'posts': Post.objects.all()
        }
        return context

class CategoryDesertListView(ListView):
    model = Post
    template_name = 'recepti/category_desert.html'
    context_object_name = 'category-desert'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = {
            'posts': Post.objects.all()
        }
        return context


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['naslov','kategorija', 'sazetak', 'sadrzaj', 'slika']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['naslov','kategorija', 'sazetak', 'sadrzaj', 'slika']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
            return True
        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

class LikeView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = []
    template_name = 'recepti/like_form.html'
    context_object_name = 'post-like'
    

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        success_url = '/post/'+ str(self.kwargs.get('pk'))
        user_id = self.request.user.id
        if not post.votes.exists(user_id):
            post.votes.up(user_id)
        return super().form_valid(form)

class DislikeView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = []
    context_object_name = 'post-dislike'
    template_name = 'recepti/dislike_form.html'
    
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        success_url = '/post/'+ str(self.kwargs.get('pk'))
        user_id = self.request.user.id
        
        post.votes.down(user_id)
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user or self.request.user == comment.post.autor:
            return True
        return False

def about(request):
    return render(request, 'recepti/about.html', {'title': 'O nama'})
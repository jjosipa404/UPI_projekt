from django.http import HttpResponse
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

from .models import Post, Comment #, Preference
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


""" @login_required
def postpreference(request, postid, userpreference):
    if request.method == "POST":
        eachpost = get_object_or_404(Post, id=postid)
        obj=''
        valueobj=''
        try:
            obj= Preference.objects.get(user= request.user, post= eachpost)
            valueobj= obj.value #value of userpreference
            valueobj= int(valueobj)
            userpreference= int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref= Preference()
                upref.user= request.user
                upref.post= eachpost
                upref.value= userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                    eachpost.dislikes += 1
                    eachpost.likes -= 1
                    upref.save()
                    eachpost.save()
                    context= {'eachpost': eachpost,
                              'postid': postid}
                    return render (request, 'recepti/home.html')

                elif valueobj == userpreference:
                    obj.delete()   
                    if userpreference == 1:
                        eachpost.likes -= 1
                    elif userpreference == 2:
                        eachpost.dislikes -= 1

                    eachpost.save()
                    context= {'eachpost': eachpost,
                             'postid': postid}
                    return render (request, 'recepti/home.html')
                                
                        
        
                
        except Preference.DoesNotExist:
            upref= Preference()
            upref.user= request.user
            upref.post= eachpost
            upref.value= userpreference
            userpreference= int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes +=1

            upref.save()
            eachpost.save()                            
            context= {'eachpost': eachpost,
                       'postid': postid}
            return render (request, 'recepti/home.html')


    else:
        eachpost= get_object_or_404(Post, id=postid)
        context= {'eachpost': eachpost,
                  'postid': postid}

        return render (request, 'posts/detail.html', context) """

def about(request):
    return render(request, 'recepti/about.html', {'title': 'O nama'})
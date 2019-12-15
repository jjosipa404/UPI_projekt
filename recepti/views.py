from django.shortcuts import render
from django.http import HttpResponse

#posts = [
 #   {
  #      'autor':'Ana Maria',
   #     'naziv':'Kokos keksići',
    #    'sastojci':'200g kokosa, 80g šećera, 1 vanilin šećer, 50g brašna, 2 žlice praška za pecivo, 1 žlica margarina, 1 jaje',
     #   'postupak':'Sve suhe sastojke zajedno pomiješati, dodati omekšali margarin i jaje te dobro izmijesti u glatko tijesto. '+
      #   'Umotati u prozirnu foliju i ostaviti oko pola sata u hladnjak. Žličicom vaditi komade i oblikovati kuglice.' +
       #  'Staviti na lim obložn pek-papirom te malo utisnuti. Peći na 180°C oko 10-12 minuta do željene boje.' +
        # 'Ostavit da se ohlade. Po želji ukrasiti sa čokoladom.' +
         #'Smjesa je dovoljna za 50-tak komada. ',
        #'datum':'6.12.2019.'
   # },
   # {
    #    'autor':'Biserka',
     #   'naziv':'Fina kremasta juhica',
    #   'sastojci':'5-6 krumpira, 4 manje glavice luka, 1.5-2L vode,'+
     #  'Kajenski papar, maslinovo ulje, slanina, vegeta',
      #  'postupak':'Na maslinovom ulju popržiti luk dok ne pozlatni te dodati slaninu i malo popržiti.'+
       # 'Zatim dodati krumpir te dinstati uz povremeno miješanje podlijevajući vodom da ne zagori. Dodati kajenski papar i vegetu. '+
       # 'Uliti vode i kuhati dok krumpir ne omekša. Kad je krumpir skuhan, sve zajedno štapnim mikserom usitniti i još par minuta prokuhati.',
       # 'datum':'7.12.2019.'
    #}
#]

# Create your views here.
#def home(request):
 #   context = {
  #      'posts' : posts
   # }
    #return render(request, 'recepti/home.html', context)


#def about(request):
 #   return render(request, 'recepti/about.html')
    

#--------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.models import User

from django.views.generic import (

    ListView,

    DetailView,

    CreateView,

    UpdateView,

    DeleteView

)

from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'recepti/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'recepti/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'recepti/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(autor=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['naslov', 'sazetak', 'sadrzaj', 'slika']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['naslov', 'sazetak', 'sadrzaj', 'slika']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.autor:
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

def about(request):
    return render(request, 'recepti/about.html', {'title': 'O nama'})
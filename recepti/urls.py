#from django.contrib import admin
#from django.urls import path
#from . import views

#urlpatterns = [
 #   path('admin/', admin.site.urls),
  #  path('', views.home, name="recepti-home"),
   # path('about/', views.about, name="recepti-about"),
    
#]

from django.urls import path

from .views import (

    PostListView,

    PostDetailView,

    PostCreateView,

    PostUpdateView,

    PostDeleteView,

    UserPostListView

)

from . import views



urlpatterns = [

    path('', PostListView.as_view(), name='recepti-home'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    path('post/new/', PostCreateView.as_view(), name='post-create'),

    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('about/', views.about, name='recepti-about'),

]

from django.urls import path
from .views import (

    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    CategoryPredjeloListView,
    CategoryGlavnoListView,
    CategoryDesertListView,

)
from . import views
urlpatterns = [

    path('', PostListView.as_view(), name='recepti-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('posts/predjela', CategoryPredjeloListView.as_view(), name='category-predjelo'),
    path('posts/glavna', CategoryGlavnoListView.as_view(), name='category-glavno'),
    path('posts/deserti', CategoryDesertListView.as_view(), name='category-desert'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('post/comment/<int:pk>/delete', CommentDeleteView.as_view(), name='post-comment-delete'),
    path('post/comment/<int:pk>/update', CommentUpdateView.as_view(), name='post-comment-update'),
    #path('post/<int:pk>/<int:pk>/preference/<int:preference>/',views.postpreference,name='postpreference'),
    path('about/', views.about, name='recepti-about')
]

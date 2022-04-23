from django.urls import path
from . import views
import blog
from .views import(
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>', views.PostDetailView, name='post-detail'),
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    # path('', views.home, name='blog-home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('postComment/', views.postComment, name='postComment'),
    # path('comment/', views.comment, name='comment'),
]



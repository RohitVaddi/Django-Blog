  
import blog
from django.db.models import query
from django.http import request
from django.shortcuts import render, redirect
from .models import Post, Contact, BlogComment
from users.models import profile
from blog.templatetags import extras
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
def home(request):
    posts = Post.objects.all(),
    comments =  BlogComment.objects.filter(post=posts)
    context = {
        'posts': posts,
        'comments': comments
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/Post_Detail.html'
#     context_object_name = 'posts'


def PostDetailView(request, pk):    
    model = Post
    template_name = 'blog/Post_Detail.html'
    context_object_name = 'posts'
    post = Post.objects.get(pk=pk)
    user = request.user
    comments =  BlogComment.objects.filter(post=post, parent=None).order_by('-timestamp')
    replies =  BlogComment.objects.filter(post=post).exclude(parent=None).order_by('-timestamp')
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)       
    context = {
        'post': post,
        'comments': comments,
        'user': user,
        'replyDict': replyDict
    }
    return render(request, 'blog/Post_Detail.html', context)

    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields= ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields= ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        messages.success(request, "Your message has been sent successfully.")
        return redirect('home')
    return render(request, 'blog/contact.html', {'title': 'Contact'})


def index(request):
    return render(request, 'blog/index.html', {'title': 'Home'})


def search(request):
    query = request.GET['query']
    if len(query)>75 or len(query)==0:
        allPosts = Post.objects.none()
    else:
        allPoststitle = Post.objects.filter(title__icontains=query)
        allPostscontent = Post.objects.filter(content__icontains=query)
        # allPostsauthor = Post.objects.filter(author=query)
        allPosts=  allPoststitle.union(allPostscontent).order_by('-date_posted')
    if allPosts.count()==0:
        messages.warning(request, "No search result found. Please refine your query")

    param = {'allPosts': allPosts}
    return render(request, 'blog/search.html', param)
    

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postId = request.POST.get('postId')
        post = Post.objects.get(id=postId)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save() 
            messages.success(request, "Your comment has been posted successfully...")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully...")
    return redirect(f'/post/{post.pk}')
 

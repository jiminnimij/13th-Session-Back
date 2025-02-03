from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Hashtag
from django.utils import timezone
from .forms import Postform, Commentform

def add_comment(request, post_id):
  blog = get_object_or_404(Post, pk = post_id)

  if request.method == 'POST':
    form = Commentform(request.POST)

    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = blog
      comment.save()
      return redirect('detail', post_id)
    
  else:
    form = Commentform()
  return render(request, 'add_comment.html', {'form': form})


def home(request):
    posts = Post.objects
    return render(request, 'home.html', {'posts':posts})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    post_hashtag = post_detail.hashtag.all()
    return render(request, 'detail.html', {'post':post_detail, 'hashtag': post_hashtag})

def new(request):
    form=Postform() #form이라는 이름으로 폼 객체 선언
    return render(request, 'new.html', {'form': form})

def create(request):
    form = Postform(request.POST, request.FILES)
    if form.is_valid():
        new_blog=form.save(commit=False)
        new_blog.date=timezone.now()
        new_blog.save()
        hashtags = request.POST['hashtags']
        hashtag = hashtags.split(', ')

        for tag in hashtag:
           new_hashtag = Hashtag.objects.get_or_create(hashtag = tag)
           new_blog.hashtag.add(new_hashtag[0])
           print(new_hashtag[1])
        return redirect('detail', new_blog.id)
    return redirect('home')

def delete(request, post_id):
    blog_delete=get_object_or_404(Post,pk=post_id)
    blog_delete.delete()
    return redirect('home')

def update_page(request, post_id):
    blog_update=get_object_or_404(Post,pk=post_id)
    return render(request, 'update.html', {'blog_update':blog_update})

def update(request, post_id):
    blog_update=get_object_or_404(Post,pk=post_id)
    blog_update.title=request.POST['title']
    blog_update.body=request.POST['body']
    blog_update.save()
    return redirect('home')
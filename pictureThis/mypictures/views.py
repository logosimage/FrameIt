from django.shortcuts import render, get_object_or_404
from.models import Blog


def index(request):
    articles = Blog.objects.all()
    return render(request, 'mypictures/index.html',{'article':articles})
def article(request, slug):
    art = get_object_or_404(Blog, slug=slug)
    return render(request, 'mypictures/article.html', {'art':art})


def tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    art = Blog.objects.filter(tags__slug=slug)
    return render(request, 'mypictures/tags.html', {'article':art, 'tag':tag})
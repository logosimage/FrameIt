from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.contrib.auth.models import User
from .models import Blog, Tag, Image
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    articles = Blog.objects.all()
    return render(request, 'mypictures/index.html',{'article':articles})
def article(request, slug):
    art = get_object_or_404(Blog, slug=slug)
    return render(request, 'mypictures/article.html', {'art':art})


def tag(request, slug):
    tag = Tag.objects.get(slug=slug)
    art = Blog.objects.filter(tags__slug=slug)
    return render(request, 'mypictures/tag.html', {'article':art, 'tag':tag})

# def blog_list_api(request):
#     articles = serializers.serialize('json', Blog.objects.all())
#
#     return HttpResponse(articles, content_type='application/json')


def blog_list_api(request):
    articles = Blog.objects.all()

    data = []
    for art in articles:
        tags = []
        for t in art.tags.all():
            tags.append({
                'name': t.name,
                'desc': t.desc,
                'slug': t.slug,
            })
        if art.image:
            image = {'name':art.image.name,'url': art.image.img.url,'alt': art.image.alt}
        else:
            image = None
        data = {
            'title': art.title,
            'content': art.content,
            'author': art.author.username,
            'image': image,
            'slug':art.slug,
            'tag':tags
        }
    return JsonResponse(data, safe=False)


def article_api(request, slug):
    art = Blog.objects.get(slug=slug)
    tags = []
    for t in art.tags.all():
        tags.append({
            'name': t.name,
            'desc': t.desc,
            'slug': t.slug
        })
    if art.image:
        image = {'name': art.image.name, 'url': art.image.img.url, 'alt': art.image.alt}
    else:
        image = None

    data = {
        'title': art.title,
        'content': art.content,
        'author': art.author.username,
        'image': image,
        'slug': art.slug,
        'tags': tags
    }


    return JsonResponse(data, safe=False)

@login_required
def new_article(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        art = Blog()
        img = Image()

        if request.FILES.get('image', False):
            img.name = ''
            img.img = request.FILES['image']
            img.alt = request.POST.get('alt', '')
            img.save()
        art.title = request.POST.get('title', None)
        art.content = request.POST.get( 'content', None)
        art.author = User.objects.get(username=request.user.username)
        if request.FILES.get('image',False):
            art.image = img

        art.save()
        for t in request.POST.getlist('tags[]', []):
            art.tags.add(Tag.objects.get(slug=t))

        art.save()

        return HttpResponse('<h1 style="sidth: 100%; text-align: center;"> Thank you</h1>'
                     '<div><a href="http://localhost:8080">Return Home</a></div>')

    return render(request, 'mypictures/new_article.html', {'tags': tags})



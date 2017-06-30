from django.shortcuts import render, get_object_or_404
from django.core import serializers
from .models import Blog, Tag, image
from django.http import JsonResponse


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


def new_article(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        art = Blog
        img = image()

        if request.FILES.get('image', False):
            img.name = ''
            img.img = request.FILES['image']
            img.alt = request.POST.get('alt', '')
            img.save()

    return  render (request, 'pages/new_article.html',{'tags': tag} )
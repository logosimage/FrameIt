from django.contrib import admin
from .models import Blog, Image, Tag


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_tags')
    # fields = ['title', 'content', ('author','tags'),'image']
    list_filter = ('tags',)
    fieldsets = (
        ('None', {
            'fields':('title', 'content')
        }),
        ('other Stuff', {
            'fields':('author','image', "tags")
        }),
    )


admin.site.register(Blog, BlogAdmin)
admin.site.register(Image)
admin.site.register(Tag)



from django.contrib import admin

from blog.models import Post,Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'slug')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    search_fields = ('content',)
    list_filter = ('created_date', 'author')


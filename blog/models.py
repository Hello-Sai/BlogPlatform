from collections.abc import Iterable
import random
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(null=True)
    author = models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    class Meta:
        ordering = ('-published_date',)
    # def get_absolute_url(self):
    #     return reverse('')
    def __str__(self) -> str:
        return f'{self.title}'
    def save(self,*args,**kwargs) -> None:
        if not self.slug:

            self.slug = slugify(self.title+ f"{random.randint(1,9999)}")
        super().save(*args,**kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.post.title} - {self.created_date}'
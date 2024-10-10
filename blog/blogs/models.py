from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

class User(AbstractUser):
    
    email = models.EmailField(unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()  # Rich Text Editor
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
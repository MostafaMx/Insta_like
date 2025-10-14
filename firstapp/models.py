from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    phone = models.CharField(max_length=13, null=True, unique=True)
    email = models.EmailField(null=True, unique=True)
    profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class Blog(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    number_of_likes = models.PositiveIntegerField(default=0)
    number_of_dislikes = models.PositiveIntegerField(default=0)

class Reaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    TYPES = [(LIKE, 'Like'), (DISLIKE, 'Dislike')]

    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TYPES)

    class Meta:
        unique_together = ('user', 'blog')
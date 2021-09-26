import os
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"products/{instance.author}/{final_name}"


# with method of manager
class PostManager(models.Manager):
    def get_published(self):
        return self.filter(status='published')

    def get_from_year(self, year):
        return self.filter(publish__year=year)

# with the other manager
class get_drafts(models.Manager):
    # we should use thid function
    def get_queryset(self):
        return super(get_drafts, self).get_queryset().filter(status='draft')

    # show specific day of draf posts
    def get_from_day(self, day):
        return self.filter(publish__day=day)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path)
    tag = models.ManyToManyField(Tag, related_name="tag")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='published')
    published = PublishedManager()
    objects = PostManager()
    drafts = get_drafts()


    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id, self.slug])


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    body = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)


    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class Account(models.Model):
    GENDER_CHOICES = (
        ("man", "Man"),
        ("woman", "Woman")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    phone = models.CharField(max_length=13)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name



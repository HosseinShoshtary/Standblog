from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    category = models.ManyToManyField(Category, related_name="articles")
    title = models.CharField(max_length=70)
    body = models.TextField()
    image = models.ImageField(upload_to="images/article", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        ordering = ("-created",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"

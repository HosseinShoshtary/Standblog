from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Article(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="نویسنده")
    category = models.ManyToManyField(Category, related_name="articles", verbose_name="موضوع")
    title = models.CharField(max_length=70, verbose_name="تایتل")
    body = models.TextField(verbose_name="متن")
    image = models.ImageField(upload_to="images/article", blank=True, null=True, verbose_name="عکس")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    slug = models.SlugField(null=True, blank=True, unique=True, verbose_name="اسلاگ ")
    pub_date = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ("-created",)
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    # def show_image(self):
    #     return format_html(f'<img src="{self.image.url}" width="30px" height="30px" >')

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", verbose_name="مقاله")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="کاربر")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies", verbose_name="در جواب")
    body = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", varbose_name="کاربر")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes", varbose_name="مقاله")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name="تایتل")
    text = models.TextField(verbose_name="متن پیام")
    email = models.EmailField(verbose_name="ایمبل")
    age = models.IntegerField(default=0, verbose_name="سن")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateTimeField(default=timezone.now(), verbose_name="تاریخ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"




    # class Meta:
    #     verbose_name = "لایک"
    #     verbose_name_plural = "لایک ها"
    #     ordering = ("-created_at",)
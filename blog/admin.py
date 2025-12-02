from django.contrib import admin
from . import models


class FilterByTitle(admin.SimpleListFilter):
    title = "بر اساس کلید های پر تکرار"
    parameter_name = "title"

    def lookups(self, request, model_admin):
        return (
            ("django", "جنگو"),
            ("python", "پایتون")
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


class CommentInLine(admin.TabularInline):
    models = models.Comment


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    # "show_image"
    list_display = ("title", "auther", "status")
    # list_editable = ("title", "status")
    list_filter = ("status", FilterByTitle)
    search_fields = ("title", "body")
    # inlines = (CommentInLine,)
    # fields = ("title", "body")


admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(models.Message)
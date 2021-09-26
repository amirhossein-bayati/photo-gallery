from django.contrib import admin
from .models import Post, Comment, Account, Tag
from django.utils.html import format_html


def colored_name(Post):
    return format_html(f'<span style="color: #2F8DFE;">{Post.title}</span>')


colored_name.allow_tags = True


def upper_case_name(Post):
    return ("%s" % (Post.title)).upper()


@admin.action(description='Mark selected as actived')
def make_acived(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (colored_name,'slug', 'author', 'publish', 'status', 'tag_to_str')
    list_filter = ('status', 'author', 'publish')
    ordering = ('status', 'publish')
    search_fields = ('title', 'description')
    empty_value_display = '-'  # If the value of a field is None, an empty string, or an iterable without elements, Django will display - (a dash).
    prepopulated_fields = {"slug": ("title",)}  # auto fill slug from title
    raw_id_fields = ('author',)  # if you have many author and you wanna to select them with an id
    list_editable = ('status',)  # edit status in preview of post
    # list_display_links = ('slug',)  # make slug linkable to see post
    date_hierarchy = 'publish'  # time row to see post in range of date


    def tag_to_str(self, obj):
        return ", ".join([tag.name for tag in obj.tag.all()])

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'created', 'active')
    list_editable = ('active',)
    list_filter = ('post', 'name', 'active')
    search_fields = ('name', 'body')
    empty_value_display = '-'
    ordering = ('active', 'post')
    actions = [make_acived]


# admin.site.register(Account)
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender', 'created')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status')
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ('status',)

admin.site.register(Tag, TagAdmin)

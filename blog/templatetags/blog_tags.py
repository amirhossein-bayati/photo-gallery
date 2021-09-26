
from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('post/lastest_posts.html')
def show_lastest_posts(count=6):
    lastests_posts = Post.published.order_by('-publish')[:count]
    return {"lastests_posts": lastests_posts}

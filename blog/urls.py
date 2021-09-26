from django.urls import path
from . import views

from .feeds import LastetsPostsFeeds


app_name = 'blog'

urlpatterns = [
    path('', views.list_view, name='home'),
    path('posts/', views.list_view, name='list_view'),
    path('account/', views.UserAccount, name='user_account'),
    path('contact-us/', views.contactus, name='contact-us'),
    path('posts/<int:pk>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/<slug:slug>/edit', views.post_edit, name='post_edit'),
    path('feed/', LastetsPostsFeeds(), name="post_feed"),
    path('search/', views.post_search, name='post_search'),
    path('categories/<str:cat>', views.list_with_category, name="list_with_category")
]
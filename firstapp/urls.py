from django.contrib import admin
from django.urls import path, include
from .views import home, register_page, login_page, logout_page, add_blog, edit_blog, delete_blog, all_blogs,myprofile, toggle_reaction
urlpatterns = [
    path('home/', home, name='home_url'),
    path('register/', register_page, name='register_url'),
    path('login/', login_page, name='login_url'),
    path('logout/', logout_page, name='logout_url'),
    path('addblog/', add_blog, name='add_blog_url'),
    path('editblog/<int:blog_id>/', edit_blog, name='edit_blog_url'),
    path('deleteblog/<int:pk>/', delete_blog, name='delete_blog_url'),
    path('', all_blogs, name='all_blogs_url'),
    path('myprofile/',myprofile,name='myprofile'), # <-- add this line
    # path('comments/<int:blog_id>/', comments_view, name='comments'),
    path('react/<int:blog_id>/', toggle_reaction, name='toggle_reaction'),
]


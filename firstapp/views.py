from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Person, Reaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, EditBlogForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def home(request):
    search_query = request.GET.get('search', '')
    blogs = Blog.objects.filter(author=request.user)
    if search_query:
        blogs = blogs.filter(title__icontains=search_query)
    context = {'blogs': blogs}
    return render(request, 'home.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            messages.success(request,'your logged in successfully')

            return redirect('all_blogs_url')
        else:
            messages.error(request,'username or password is wrong!')
            return redirect('login_url')
    return render( request , 'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('repeatedPassword', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if not username:
            messages.error(request, 'Username is required!')
            return redirect('register_url')
        elif password1 != password2:
            messages.error(request, 'Passwords are not matching!')
            return redirect('register_url')
        elif Person.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists!')
            return redirect('register_url')
        elif Person.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register_url')
        elif Person.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register_url')
        user = Person.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password1,
        )
        user.save()
        messages.success(request, 'Registration successful!')
        return redirect('login_url')
    return render(request, 'register.html')


@login_required    
def logout_page(request):
    logout(request)
    return redirect('login_url')

@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog added successfully!')
            return redirect('home_url')
    else:
        form = BlogForm()
    return render(request, 'addblog.html', {'form': form})


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = EditBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('home_url')
        blog.image = request.FILES.get('image', blog.image)
        blog.save()
        messages.success(request, 'Blog updated successfully!')
    else:
        form = EditBlogForm(instance=blog)
    return render(request, 'editblog.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if not request.user == blog.author:
        return HttpResponse('403')
    blog.delete()
    messages.success(request, 'blog deleted')
    return redirect('home_url')

# def all_blogs(request):
#     blogs = Blog.objects.all().order_by('-created_at')
#     return render(request, 'allblogs.html', {'blogs': blogs})

@login_required
def myprofile(request):
    user = request.user  # اینجا از Person هست
    if request.method == 'POST':
        if 'profilepic' in request.FILES:
            user.profilepic = request.FILES['profilepic']
            user.save()
            messages.success(request, 'Profile picture updated successfully!')
        return redirect('myprofile')
    return render(request, 'myprofile.html', {'person': user})


# @login_required
# def comments_view(request, blog_id):
#     blog = get_object_or_404(Blog, id=blog_id)
#     comments = Comment.objects.filter(post=blog)
#     return render(request, 'comments.html', {'blog': blog, 'comments': comments})
#     if request.method == 'POST':
#         text = request.POST.get('text')
#         parent_id = request.POST.get('parent_id')
#         parent_comment = Comment.objects.get(id=parent_id) if parent_id else None
#         new_comment = Comment.objects.create(
#             user=request.user,
#             blog=blog,
#             text=text,
#             parent=parent_comment
#         )
#         new_comment.save()
#         messages.success(request, 'Comment added successfully!')
#         return redirect('comments', blog_id=blog.id)
    















@login_required
def toggle_reaction(request, blog_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    reaction_type = request.POST.get('type')
    if reaction_type not in ['like', 'dislike']:
        return JsonResponse({'error': 'Invalid reaction type'}, status=400)

    blog = get_object_or_404(Blog, id=blog_id)

    reaction, created = Reaction.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        if reaction.type == reaction_type:
            reaction.delete()
            if reaction_type == 'like':
                blog.number_of_likes = max(0, blog.number_of_likes - 1)
            else:
                blog.number_of_dislikes = max(0, blog.number_of_dislikes - 1)
            active = None
        else:
            if reaction.type == 'like':
                blog.number_of_likes = max(0, blog.number_of_likes - 1)
            else:
                blog.number_of_dislikes = max(0, blog.number_of_dislikes - 1)
            reaction.type = reaction_type
            reaction.save()
            if reaction_type == 'like':
                blog.number_of_likes += 1
            else:
                blog.number_of_dislikes += 1
            active = reaction_type
    else:
        reaction.type = reaction_type
        reaction.save()
        if reaction_type == 'like':
            blog.number_of_likes += 1
        else:
            blog.number_of_dislikes += 1
        active = reaction_type

    blog.save()

    return JsonResponse({
        'likes': blog.number_of_likes,
        'dislikes': blog.number_of_dislikes,
        'active': active
    })
from django.core.paginator import Paginator
def all_blogs(request):
    search_query = request.GET.get('search', '')
    blogs = Blog.objects.all().order_by('-created_at')

    if search_query:
        blogs = blogs.filter(title__icontains=search_query)

    if request.user.is_authenticated:
        for blog in blogs:
            reaction = Reaction.objects.filter(user=request.user, blog=blog).first()
            blog.reaction_type = reaction.type if reaction else None
    else:
        for blog in blogs:
            blog.reaction_type = None

    paginator = Paginator(blogs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
        'count': blogs.count(),
        'search_query': search_query,
    }
    return render(request, 'allblogs.html', context)


# def all_blogs(request):
#     blogs = Blog.objects.all().order_by('-created_at')
#     return render(request, ss'allblogs.html', {'blogs': blogs})
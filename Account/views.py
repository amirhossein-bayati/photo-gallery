from time import sleep

from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm, ChangePass, RegisterForm, AddPhotoForm
from blog.models import Tag, Post
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required

from blog.models import Post


def user_login(request):
    # If User Logged In Before
    if request.user.is_authenticated:
        return redirect("blog:list_view")

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():

            # Get Form Data
            cd = form.cleaned_data
            username = cd["username"]
            password = cd["password"]

            # Authenticate User
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:list_view')

                else:
                    messages.error(request, message=f"Disabled Account")
            else:
                messages.error(request, message=f"Invalid Login")
    else:
        form = LoginForm()

    return render(request, 'account/forms/login.html', {'form': form})


def register_user(request):
    # If User Logged In Before
    if request.user.is_authenticated:
        return redirect("blog:list_view")

    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            # Get Form Data
            cd = register_form.cleaned_data
            username = cd["username"]
            password = cd["password"]
            email = cd["email"]

            # Create User
            user = User.objects.create_user(username=username, password=password, email=email)
            # Save Created User
            user.save()
            return redirect('account:user_login')
    else:
        register_form = RegisterForm()

    return render(request, 'account/forms/register.html', {"form": register_form})


@login_required
def user_logout(request):
    # LogOut User
    logout(request)
    return render(request, 'account/views/logged_out.html')


@login_required
def password_change(request):
    user = request.user
    form = ChangePass()

    if request.method == "POST":
        form = ChangePass(request.POST)

        if form.is_valid():
            # Get Form Data
            cd = form.cleaned_data
            last_password = cd["last_password"]
            # Check Last Password
            check_password = user.check_password(last_password)

            # If Passwords Are The Same
            if check_password:
                new_password = cd["new_password"]
                # Set New Password
                user.set_password(new_password)
                user.save()

                return redirect('account:user_login')
            else:
                messages.error(request, "Your Password Not Mached")
    else:
        form = ChangePass()
    return render(request, 'account/views/change_password.html', {'form': form})


@login_required
def profile(request):
    photoForm = AddPhotoForm()

    # Get USer
    user = request.user

    # Get User Posts
    posts = user.blog_posts.filter(status='published')

    # Get Categories
    categories = Tag.objects.filter(status=True)

    # Add New Photo Form
    if request.method == "POST":
        photoForm = AddPhotoForm(data=request.POST)
        if photoForm.is_valid():
            # Get Form Data
            cd = photoForm.cleaned_data
            title = cd["title"]
            description = cd["description"]
            slug = title.replace(" ", "-")
            tag = Tag.objects.get(id=cd['tag'])
            image = request.FILES.get('image')

            # Create New Object
            myPost = Post.objects.create(title=title, author=user, description=description, image=image, slug=slug)
            myPost.tag.add(tag)

            return redirect('account:profile')
    return render(request, 'profile/base/profile.html', {'user': user, 'posts': posts, 'photoForm': photoForm, 'categories':  categories})
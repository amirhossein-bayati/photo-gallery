from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from .models import Post, Account, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, AccountForm, ContactusForm, SharePostForm, SearchForm
from Account.forms import AddPhotoForm
from django.core.mail import send_mail

from django.contrib import messages

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Tag

from django.contrib.auth.decorators import login_required



def list_view(request):
    # Get All Published Posts
    posts = Post.published.all()

    # Get All Available Categories
    categories = Tag.objects.filter(status=True)

    # Paginate Site With 6 Items Per A Page
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')

    # Post Of Certain Page
    try:
        posts = paginator.page(page)

    # If Page Not Integer
    except PageNotAnInteger:
        posts = paginator.page(1)

    # If Page NOt Exists
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'partials/content.html', {'posts': posts, 'page': page, 'categories': categories})


def post_detail(request, pk, slug):
    user = request.user
    post = Post.objects.get(slug=slug, id=pk)
    comments = post.comments.filter(active=True)

    # To Understand Email Sent
    sent = False

    # For New Comment
    new_comment = None

    # Handle The Forms
    if request.method == 'POST':
        # Define Forms
        share_form = SharePostForm()
        comment_form = CommentForm()
        # Handle Share Post Form
        if "shareForm" in request.POST:
            # Create Object Of ShareForm
            share_form = SharePostForm(request.POST)
            if share_form.is_valid():
                email = share_form.cleaned_data['email']
                subject = post.title
                link = request.build_absolute_uri(post.get_absolute_url())
                message = f"post \"{subject}\" sent to you \n link: {link}"
                # Send An Email To User
                send_mail(subject, message, 'EMAIL ADDRESS', {email}, fail_silently=False)
                sent = True

                messages.warning(request, message="Email Has Been Sent")
                return redirect(reverse('blog:post_detail', args=[pk, slug]))
            else:
                share_form = SharePostForm()

        # Handle Comment Form
        if "commentForm" in request.POST:
            # A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # Save the comment to the database
                new_comment.save()

                messages.success(request, message=f"Successfully Commented")

                return redirect(reverse('blog:post_detail', args=[pk, slug]))
            else:
                comment_form = CommentForm()
    else:
        share_form = SharePostForm()
        comment_form = CommentForm()

    context = {
        'post': post,
        'share_form': share_form,
        'sent': sent,
        'comment_form': comment_form,
        'comments': comments,
        'user': user,
    }
    return render(request, 'post/post_detail.html', context)


@login_required
def post_edit(request, pk, slug):
    post = Post.published.get(id=pk, slug=slug)
    categories = Tag.objects.filter(status=True)

    # Get Current Post Category
    curent_cat = str(post.tag.first())

    if request.method == "POST":
        # To Delete Post
        if "delete" in request.POST:
            post.delete()
            return redirect('account:profile')

        photoForm = AddPhotoForm(data=request.POST)
        if photoForm.is_valid():

            # Get User Form Data
            cd = photoForm.cleaned_data
            title = cd["title"]
            description = cd["description"]
            slug = title.replace(" ", "-")
            tag = Tag.objects.get(id=cd['tag'])

            # Save New Data On Post
            post.title = title
            post.description = description
            post.slug = slug
            post.tag.add(tag)

            # Save And Update Post
            post.save()

            return redirect('account:profile')
    else:
        photoForm = AddPhotoForm()
    return render(request, 'post/post_edit.html', {'post': post, 'categories':categories, 'curent_cat': curent_cat})


@login_required
def UserAccount(request):
    user = request.user

    # Get User Account If Exists
    try:
        account = Account.objects.get(user=user)

    # Create User Account If Not Exists
    except:
        account = Account.objects.create(user=user)

    if request.method == "POST":
        form = AccountForm(data=request.POST)
        if form.is_valid():

            # Get And Save New Data
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data["email"]
            account.gender = form.cleaned_data['gender']
            account.address = form.cleaned_data['address']
            account.age = form.cleaned_data['age']
            account.phone = form.cleaned_data['phone']

            # Save And Update User And Account
            user.save()
            account.save()

            return redirect('blog:list_view')

        else:
            return render(request, 'blog/forms/account_form.html', {'form': form, 'account': account})
    form = AccountForm()
    return render(request, 'blog/forms/account_form.html', {'form': form, 'account': account})


def contactus(request):
    # To Understand Email Sent
    sent = False
    if request.method == "POST":
        form = ContactusForm(request.POST)
        if form.is_valid():

            # Get User Form Data
            cd = form.cleaned_data
            name = cd['name']
            subject = cd['subject']
            email = cd['email']
            phone = cd['phone']
            message = cd['message']
            text = f"from: {name}\nemail: {email}\nphone: {phone}\nmessage: {message}"

            # Send Email To Admin
            send_mail(subject, text, 'EMAIL ADDRESS', ['amirsmvb@gmail.com'], fail_silently=False)

            # Email Sent
            sent = True

            # Send Success Message To Template
            messages.success(request, "Thanks! Your Meesage Sent.")

            return redirect('blog:contact-us')
    else:
        form = AccountForm()
    return render(request, 'blog/forms/contactus_form.html', {'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm()
    # Phrase That User Search
    query = None

    # Founded Results
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]

            # Search In Posts
            search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    context = {
        'query': query,
        'posts': results,
        'form': form
    }
    return render(request, 'partials/content.html', context)


def list_with_category(request, cat):
    # Get Published Posts With Specific Categories
    posts = Post.published.filter(tag__name=cat)

    # To Show All Posts
    if cat == "all":
        posts = Post.published.all()

    # Paginating Pages
    paginator = Paginator(posts, 6)
    categories = Tag.objects.filter(status=True)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'partials/content.html', {'posts': posts, 'page': page, 'categories': categories, 'current_cat': cat})




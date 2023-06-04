from django.shortcuts import render
from .models import Post

from .forms import PostForm

from django.shortcuts import render
from .forms import PostForm
from .models import Post
import itertools
import random
from django.http import HttpResponseRedirect

def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))  # 'home' is the name of your URL pattern
    else:
        form = PostForm()

    colors = ['yellow', 'pink', 'green', 'orange', 'blue']
    shuffled_colors = list(itertools.islice(itertools.cycle(colors), 150))  # Adjust 150 as per your need
    random.shuffle(shuffled_colors)

    if request.user.is_authenticated:
        posts = Post.objects.exclude(user=request.user).exclude(likes=request.user).order_by('-created_at')
        template = 'loggedin.html'
    else:
        posts = Post.objects.all().order_by('-created_at')
        template = 'home.html'

    context = {
        'form': form,
        'posts': posts,
        'shuffled_colors': shuffled_colors,
    }

    return render(request, template, context)








from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileForm

from django.http import JsonResponse

from django.contrib.auth import login, authenticate
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileForm(request.POST, request.FILES)
        
        # check if both forms are valid before saving anything
        if u_form.is_valid() and p_form.is_valid():
            # save User first without commiting
            user = u_form.save(commit=False)
            
            # save profile with reference to User
            profile = p_form.save(commit=False)
            profile.user = user

            # now we can safely save both User and Profile
            user.save()
            profile.save()

            # authenticate the user and log them in
            authenticated_user = authenticate(username=user.username, 
                                              password=request.POST['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                return JsonResponse({'status': 'success', 'redirect': reverse('home')})

            return JsonResponse({'status': 'success'})
        else:
            errors = dict()
            for key, value in u_form.errors.as_data().items():
                errors[key] = value[0].message
            for key, value in p_form.errors.as_data().items():
                errors[key] = value[0].message
            return JsonResponse({'errors': errors})
    else:
        u_form = UserRegisterForm()
        p_form = ProfileForm()
    return render(request, 'register.html', {'u_form': u_form, 'p_form': p_form})


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

from django.shortcuts import get_object_or_404, render
from .models import Post



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        # verify password
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
from .forms import ProfileUpdateForm

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Profile, Post

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Post

def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
    }
    
    return render(request, 'profile.html', context)

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm  # make sure you have this line

def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('view_profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': u_form,
        'profile_form': p_form
    }

    return render(request, 'edit_profile.html', context)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    

    if post.likes.filter(id=request.user.id).exists():
        # User has already liked this post
        # remove like/user
        post.likes.remove(request.user)
        is_liked = False
    else:
        # User has not liked this post
        post.likes.add(request.user)
        is_liked = True
    return JsonResponse({'isLiked': is_liked, 'likesCount': post.likes.count()}, safe=False)









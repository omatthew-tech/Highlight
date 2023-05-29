from django.shortcuts import render
from .models import Post

from .forms import PostForm

from django.shortcuts import render
from .forms import PostForm
from .models import Post
import itertools
import random

def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    colors = ['yellow', 'pink', 'green', 'orange', 'blue']
    shuffled_colors = list(itertools.islice(itertools.cycle(colors), 150))  # Adjust 150 as per your need
    random.shuffle(shuffled_colors)

    posts = Post.objects.all().order_by('-created_at')
    template = 'loggedin.html' if request.user.is_authenticated else 'home.html'

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

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {'post': post})

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




def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile') # Assuming the name of the profile view is 'profile'
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})



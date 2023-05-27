from django.shortcuts import render
from .models import Post

from .forms import PostForm

def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')
    template = 'loggedin.html' if request.user.is_authenticated else 'home.html'
    return render(request, template, {'form': form, 'posts': posts})





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

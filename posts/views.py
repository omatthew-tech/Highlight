from django.shortcuts import render
from .models import Post

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import random
import itertools
from .models import Post
from .forms import PostForm
from django.contrib import messages  # Don't forget to import messages

def home(request):
    can_post = True
    form = PostForm()

    if request.user.is_authenticated:
        if Post.objects.filter(user=request.user, created_at__gte=timezone.now()-timedelta(weeks=1)).exists():
            can_post = False

        if request.method == 'POST':
            if can_post:
                form = PostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user = request.user
                    post.save()
                    messages.info(request, "You have successfully posted. You can post again next Sunday at 3:00 PM EST.")
                    return HttpResponseRedirect(reverse('home'))  # 'home' is the name of your URL pattern
            else:
                messages.info(request, "You have already made a post this week. New post form will be available next Sunday at 3:00 PM EST.")

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
        'can_post': can_post,
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
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user)
    are_friends = request.user.profile.friends.filter(user=profile_user).exists()
    
    friend_request_sent = FriendRequest.objects.filter(
        from_profile=request.user.profile, 
        to_profile=Profile.objects.get(user=profile_user),
        status='pending'
    ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'are_friends': are_friends,
        'friend_request_sent': friend_request_sent,  # add this line
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


from .forms import UserSearchForm
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.conf import settings

def search(request):
    query = request.GET.get('query')
    if query:
        results = User.objects.annotate(
            full_name=Concat('first_name', V(' '), 'last_name'),
            full_name_reversed=Concat('last_name', V(' '), 'first_name')
        ).filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(full_name__icontains=query) |
            Q(full_name_reversed__icontains=query)
        )
        results = results.values('username', 'first_name', 'last_name', 'profile__image')
        results = [
            {
                **user,
                'profile__image': request.build_absolute_uri(settings.MEDIA_URL + user['profile__image']) 
                                if user['profile__image'] is not None else None
            }
            for user in results
]

    else:
        results = User.objects.none()

    return JsonResponse(list(results), safe=False)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, FriendRequest

@login_required
def send_friend_request(request, username):
    if request.method == 'POST':
        to_user = get_object_or_404(User, username=username)
        to_profile = get_object_or_404(Profile, user=to_user)
        from_profile = Profile.objects.get(user=request.user)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_profile=from_profile,
            to_profile=to_profile)
        if created:
            return JsonResponse({'status': 'Friend request sent.'}, status=200)
        else:
            return JsonResponse({'status': 'Friend request already sent.'}, status=200)
    else:
        return JsonResponse({'status': 'Not a POST request.'}, status=400)


@login_required
def accept_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_profile.user == request.user:
            friend_request.to_profile.add_friend(friend_request.from_profile)
            friend_request.status = 'accepted'
            friend_request.save()
            return JsonResponse({'status': 'Friend request accepted.'}, status=200)
        else:
            return JsonResponse({'status': 'Not your request to accept.'}, status=400)
    else:
        return JsonResponse({'status': 'Not a POST request.'}, status=400)

@login_required
def view_friend_requests(request):
    # Get all friend requests where the current user is the target
    friend_requests = FriendRequest.objects.filter(to_profile=request.user.profile, status='pending')
    return render(request, 'friend_requests.html', {'friend_requests': friend_requests})


@login_required
def respond_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if action == 'accept':
        if friend_request.to_profile == request.user.profile:
            # add the friend to profile
            friend_request.to_profile.friends.add(friend_request.from_profile) 
            friend_request.status = 'accepted'  # Accepted
            friend_request.save()
            messages.success(request, f"You are now friends with {friend_request.from_profile.user.username}!")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': "This friend request doesn't belong to you."})

    elif action == 'decline':
        if friend_request.to_profile == request.user.profile:
            friend_request.status = 'rejected'  # Declined
            friend_request.save()
            messages.success(request, f"You declined the friend request from {friend_request.from_profile.user.username}.")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': "This friend request doesn't belong to you."})

    else:
        return JsonResponse({'success': False, 'message': 'Invalid action.'})














from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import Movie, MovieList
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import re

# Create your views here.
@login_required(login_url='login')
def index(request):
    # Retrieve all movies and the last movie as the featured one
    movies = Movie.objects.all()
    featured_movie = movies.last()  # This fetches the last movie more efficiently

    context = {
        'movies': movies,
        'featured_movie': featured_movie,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details
    }

    return render(request, 'movie.html', context)

@login_required(login_url='login')
def genre(request, pk):
    
    movie_genre = pk
    movies = Movie.objects.filter(genre=movie_genre)

    context = {
        'movies': movies,
        'movie_genre': movie_genre,
    }
    return render(request, 'genre.html', context)


@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains=search_term)

        context = {
            'movies': movies,
            'search_term': search_term,
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')

@login_required(login_url='login')
def my_list(request):

    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []

    for movie in movie_list:
        user_movie_list.append(movie.movie)

    context = {
        'movies': user_movie_list
    }
    return render(request, 'my_list.html', context)

@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list,created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

        if created:
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already in list'}

        return JsonResponse(response_data)
    else:
        # return error
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        # Use get() to avoid the KeyError
        email = request.POST.get('email')
        username = request.POST.get('username')
        password0 = request.POST.get('password0')
        password1 = request.POST.get('password1')

        # Check if email, username, and passwords are provided
        if not email or not username or not password0 or not password1:
            messages.info(request, 'Please fill in all fields.')
            return redirect('signup')

        # Check if passwords match
        if password0 != password1:
            messages.info(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already taken.')
            return redirect('signup')

        # Check if username is already taken
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken.')
            return redirect('signup')

        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password0)
            user.save()

            # Log user in
            user_login = auth.authenticate(username=username, password=password0)
            auth.login(request, user_login)

            return redirect('/')  # Redirect to homepage or dashboard after successful signup
    else:
        return render(request, 'signup.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
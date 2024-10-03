from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm,ProfileForm, FoodPhotoForm,FoodPhotoFormSet
from .models import Recipe, RecipeRating
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.paginator import Paginator
import json
from django.db import models
from django.views import View
from .models import Recipe, FoodPhoto

from django.forms import modelformset_factory
import re

def index(request):
    return render(request, 'index.html')


@login_required
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        new_bio = request.POST.get('bio')
        if new_bio:  # If a new bio is provided, update it
            profile.bio = new_bio
            profile.save()
        return redirect('profile')  # Refresh the page after saving

    return render(request, 'profile.html', {
        'profile': profile
    })

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def delete_profile(request):
    return render(request, 'delete_profile.html')

@login_required
def confirm_delete_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.delete()
        # Optionally, delete the user account as well
        # request.user.delete()
        return redirect('index')


@login_required
def upload_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        photo_formset = FoodPhotoFormSet(request.POST, request.FILES)

        if form.is_valid() and photo_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Associate the recipe with the current user
            recipe.save()  # Save the recipe to the database

            # Save each photo in the formset
            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('image'):
                    FoodPhoto.objects.create(recipe=recipe, image=photo_form.cleaned_data['image'])

            return redirect('recipe_list')  # Redirect after saving the recipe and photos

    else:
        form = RecipeForm()
        photo_formset = FoodPhotoFormSet(queryset=FoodPhoto.objects.none())  # Empty queryset for the formset

    return render(request, 'upload_recipe.html', {
        'form': form,
        'photo_formset': photo_formset,
    })


@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(user=request.user)

    # Attach user ratings to each recipe
    for recipe in recipes:
        # Get the user's rating for this recipe
        user_rating = RecipeRating.objects.filter(user=request.user, recipe=recipe).values_list('rating', flat=True).first()
        recipe.user_rating = user_rating if user_rating is not None else 0

    # Paginate the recipes, 5 per page
    paginator = Paginator(recipes, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipe_list.html', {'page_obj': page_obj})

def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Check if the recipe belongs to the logged-in user
    if recipe.user != request.user:
        return redirect('recipe_list')  # or raise permission error

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')  # Redirect after saving
    else:
        form = RecipeForm(instance=recipe)  # Load existing recipe data

    return render(request, 'edit_recipe.html', {'form': form, 'recipe': recipe})

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)  # Assuming you're using UserCreationForm
        email = request.POST.get('email')  # Get the email from the POST data
        
        if user_form.is_valid():
            user = user_form.save()
            # Create the Profile instance for the user and save the email
            Profile.objects.create(user=user, email=email)
            login(request, user)  # Automatically log in the user after registration
            return redirect('profile')  # Redirect to the profile page

    else:
        user_form = UserCreationForm()
    
    return render(request, 'register.html', {'form': user_form})

def get_user_rating_for_recipe(user, recipe):
    try:
        rating = RecipeRating.objects.get(user=user, recipe=recipe)
        return rating.rating  # Assuming `rating` is the field storing the user's rating
    except RecipeRating.DoesNotExist:
        return 0  # Return 0 if no rating found


def search_recipes(request):
    ingredient = request.GET.get('ingredient', '')
    message = ""  # Initialize the message variable
    recipes = []  # Initialize an empty list for recipes

    # Check if the input is valid: at least 3 letters, no numbers
    if len(ingredient) >= 3 and re.match("^[a-zA-Z\s]*$", ingredient):   
        
        recipes = Recipe.objects.filter(ingredients__icontains=ingredient).order_by('title')
    else:
        message = "Please input a valid ingredient."  

    # Paginate the results if there are any recipes
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'recipes': page_obj,  
        'page_obj': page_obj,
        'message': message,  
        'query': ingredient,  
    })

def rate_recipe(request, recipe_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating_value = data.get('rating')
        recipe = Recipe.objects.get(id=recipe_id)

        # Check if the user is trying to rate their own recipe
        if recipe.user == request.user:
            return JsonResponse({'error': 'You cannot rate your own recipe.'}, status=403)

        # Update or create the rating
        RecipeRating.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={'rating': rating_value}
        )

        # Update the average rating
        average_rating = RecipeRating.objects.filter(recipe=recipe).aggregate(models.Avg('rating'))['rating__avg'] or 0
        recipe.average_rating = average_rating
        recipe.save()

        return JsonResponse({'success': True, 'new_average': average_rating})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'ratings.html', {
        'recipe': recipe,
        'user_is_authenticated': request.user.is_authenticated
    })

@login_required

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe,id=recipe_id,user=request.user)
    recipe.delete()
    return redirect('recipe_list')

@login_required
def edit_profile(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile after saving
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'profile.html', {
        'profile': user_profile,  # Pass the profile object for displaying
        'form': form,
    })


class DeleteProfileView(View):
    def get(self, request):
        return render(request, 'delete_profile.html')

    def post(self, request):
        if request.user.is_authenticated:
            user_profile = request.user.profile
            user_profile.delete()  # Deletes the Profile instance
            request.user.delete()  # Deletes the User instance
            logout(request)  # Log out the user
            return redirect('register')  # Redirect to the registration page
        return redirect('profile')

def update_bio(request):
    if request.method == 'POST' and request.user.is_authenticated:
        bio = request.POST.get('bio')
        profile = request.user.profile
        profile.bio = bio
        profile.save()
        return redirect('profile')
    return redirect('profile')

@login_required
def delete_profile_photo(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.photo.delete(save=False)  # Delete the photo file
        profile.photo = None  # Clear the photo field
        profile.save()  # Save the profile changes
        return redirect('profile') 
    
@login_required
def upload_food_photo(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        form = FoodPhotoForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Manually handle multiple file uploads
            images = request.FILES.getlist('image')  # Get the list of uploaded images
            for image in images:
                FoodPhoto.objects.create(recipe=recipe, image=image)  # Save each image linked to the recipe
                
            return redirect('recipe_list')  # Redirect after successful upload

    else:
        form = FoodPhotoForm()

    return render(request, 'upload_food_photo.html', {'form': form, 'recipe': recipe})

@login_required
def delete_photo(request, photo_id):
    # Get the photo object
    photo = get_object_or_404(FoodPhoto, id=photo_id)

    if request.method == "POST":
        # Delete the photo
        photo.delete()
        # Redirect back to the recipe list page
        return redirect('recipe_list')  # Ensure 'recipe_list' matches your URL name

    # If not POST, redirect or return some other response
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
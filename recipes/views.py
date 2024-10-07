from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm,ProfileForm, FoodPhotoForm,FoodPhotoFormSet
from .models import Recipe, RecipeRating, FoodPhoto
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.paginator import Paginator
from django.contrib import messages
import json
from django.db import models
from django.views import View
import re
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        email = request.POST.get('email', '').strip()  # Get the email from the POST data

        if user_form.is_valid():
            user = user_form.save()

            # Save email to the user's profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.email = email  # Set the email in the profile
            profile.save()  # Save the profile

            # Automatically log in the user after registration
            login(request, user)
            return redirect('profile')  # Redirect to the profile page
    else:
        user_form = UserCreationForm()

    return render(request, 'register.html', {'form': user_form})


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

        # Check if both the recipe form and photo formset are valid
        if form.is_valid() and photo_formset.is_valid():
            # Save the recipe instance
            recipe = form.save(commit=False)
            recipe.user = request.user  # Associate the recipe with the current user
            recipe.save()  # Save the recipe to the database

            # Save each photo in the formset
            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('image'):
                    FoodPhoto.objects.create(recipe=recipe, image=photo_form.cleaned_data['image'])

            return redirect('recipe_list')  # Redirect to the recipe list view

        # If the form is invalid, you can still return the form with errors
    else:
        form = RecipeForm()
        photo_formset = FoodPhotoFormSet(queryset=FoodPhoto.objects.none())  # Empty queryset for the formset

    # Render the upload recipe template with the form and formset
    return render(request, 'upload_recipe.html', {
        'form': form,
        'photo_formset': photo_formset,
    })


@login_required
def recipe_list(request):
    # Retrieve recipes, ordered by most recent (assuming you have a 'created_at' field)
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')

    # Attach user ratings to each recipe
    for recipe in recipes:
        # Get the user's rating for this recipe
        user_rating = RecipeRating.objects.filter(user=request.user, recipe=recipe).values_list('rating', flat=True).first()
        recipe.user_rating = user_rating if user_rating is not None else 0

    # Paginate the recipes, 2 per page
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


def get_user_rating_for_recipe(user, recipe):
    try:
        rating = RecipeRating.objects.get(user=user, recipe=recipe)
        return rating.rating  # Assuming `rating` is the field storing the user's rating
    except RecipeRating.DoesNotExist:
        return 0  # Return 0 if no rating found


def search_recipes(request):
    ingredient = request.GET.get('ingredient', '')
    message = ""
    recipes = []  # Initialize an empty list for recipes

    # Check if the input is valid: at least 3 letters, no numbers
    if len(ingredient) >= 3 and re.match("^[a-zA-Z\s]*$", ingredient):
        recipes = Recipe.objects.filter(ingredients__icontains=ingredient).order_by('title')
    else:
        message = "Please input a valid ingredient."

    # Paginate the results if there are any recipes
    paginator = Paginator(recipes, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'recipes': page_obj,
        'page_obj': page_obj,
        'message': message,
        'query': ingredient,
        'user': request.user,  # Pass the current user to the template
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

        # Round the average rating to one decimal place
        average_rating = round(average_rating, 2)
        
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
            # Save the profile form
            form.save()

            # Update the email from the POST data
            email = request.POST.get('email', '').strip()
            user_profile.email = email  # Update the email field in the profile
            user_profile.save()  # Save the profile again to include the email change
            
            return redirect('profile')  # Redirect to profile after saving
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {  # Change to 'edit_profile.html' to show the edit form
        'profile': user_profile,  # Pass the profile object for displaying
        'form': form,
    })


class DeleteProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'delete_profile.html')

    def post(self, request):
        user_profile = request.user.profile
        user_profile.delete()  # Deletes the Profile instance
        request.user.delete()  # Deletes the User instance
        logout(request)  # Log out the user
        return redirect('register')

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
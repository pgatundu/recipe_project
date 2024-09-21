from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe, RecipeRating
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.paginator import Paginator
import json
from django.db import models


def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')



@login_required
def upload_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Assign the current user to the recipe
            recipe.save()
            return redirect('recipe_list')  # Redirect to a page after saving
    else:
        form = RecipeForm()
    return render(request, 'upload_recipe.html', {'form': form})

@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(user=request.user)

    # Attach user ratings to each recipe
    for recipe in recipes:
        # Get the user's rating for this recipe
        user_rating = RecipeRating.objects.filter(user=request.user, recipe=recipe).values_list('rating', flat=True).first()
        recipe.user_rating = user_rating if user_rating is not None else 0

    # Paginate the recipes, 5 per page
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipe_list.html', {'page_obj': page_obj})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('profile')  # Redirect to profile or another page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def get_user_rating_for_recipe(user, recipe):
    try:
        rating = RecipeRating.objects.get(user=user, recipe=recipe)
        return rating.rating  # Assuming `rating` is the field storing the user's rating
    except RecipeRating.DoesNotExist:
        return 0  # Return 0 if no rating found


def search_recipes(request):
    ingredient = request.GET.get('ingredient', '')
    recipes = Recipe.objects.filter(ingredients__icontains=ingredient).order_by('title')

    # Paginate the results
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    results = []
    for recipe in page_obj:
        # Get the user's rating if available
        user_rating = RecipeRating.objects.filter(recipe=recipe, user=request.user).first()
        user_rating_value = user_rating.rating if user_rating else 0
        results.append({
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'description': recipe.description,
            'instructions': recipe.instructions,
            'average_rating': recipe.average_rating,
            'user_rating': user_rating_value,
        })

    return render(request, 'search.html', {
        'recipes': results,
        'page_obj': page_obj,
    })

from django.http import JsonResponse

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
        ratings = RecipeRating.objects.filter(recipe=recipe)
        average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
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
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    return redirect('recipe_list')

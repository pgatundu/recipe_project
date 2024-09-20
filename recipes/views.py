from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Profile





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
    return render(request, 'recipe_list.html', {'recipes': recipes})

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

def search_recipes(request):
    ingredient = request.GET.get('ingredient', '')
    recipes = []
    if ingredient:
        # Filter recipes by ingredients (case-insensitive)
        recipes = Recipe.objects.filter(ingredients__icontains=ingredient)
    
    context = {
        'recipes': recipes,
        'ingredient': ingredient
    }
    return render(request, 'search.html', context)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    return redirect('recipe_list')

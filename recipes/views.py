from django.shortcuts import render, redirect
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
    if ingredient:
        # Assuming your model has an 'ingredients' field
        recipes = Recipe.objects.filter(ingredients__icontains=ingredient)
        results = [{'title': recipe.title, 'description': recipe.description} for recipe in recipes]
    else:
        results = []

    return JsonResponse(results, safe=False)

def some_view(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Handle the case where the profile doesn't exist
            profile = None
    # Continue with the rest of the view

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Add this to point to your index page
    path('register/', views.register, name='register'),
    path('upload/', views.upload_recipe, name='upload_recipe'),
    path('my_recipes/', views.recipe_list, name='recipe_list'),
    path('search_recipes/', views.search_recipes, name='search_recipes'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    
]

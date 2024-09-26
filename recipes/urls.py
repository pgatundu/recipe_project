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
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('rate_recipe/<int:recipe_id>/', views.rate_recipe, name='rate_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('delete_profile/', views.DeleteProfileView.as_view(), name='delete_profile'),
    path('update_bio/', views.update_bio, name='update_bio'),
    path('delete_profile_photo/', views.delete_profile_photo, name='delete_profile_photo'),
    path('upload_food_photo/<int:recipe_id>/', views.upload_food_photo, name='upload_food_photo'),
    path('delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),


   
]

from django.contrib import admin
from .models import Recipe, Profile
from django.utils.html import format_html

# Custom Profile admin class
class ProfileAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin panel
    list_display = ['user', 'bio', 'email', 'photo']
    
    # Fields to edit in the admin form
    fields = ['user', 'bio', 'email', 'photo']
    
    # Optionally, you can add search and filter options
    search_fields = ['user__username', 'email']
    list_filter = ['user']

# Custom Recipe admin class
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'average_rating', 'display_food_photo')

    def display_food_photo(self, obj):
        if obj.food_photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.food_photo.url)
        return "No photo"
    display_food_photo.short_description = 'Food Photo'

# Register the models with their custom admin classes
admin.site.register(Recipe, RecipeAdmin)  # Registering Recipe with RecipeAdmin
admin.site.register(Profile, ProfileAdmin)  # Registering Profile with ProfileAdmin

from django.contrib import admin
from .models import Recipe,  Profile


class ProfileAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin panel
    list_display = ['user', 'bio', 'email', 'photo']
    
    # Fields to edit in the admin form
    fields = ['user', 'bio', 'email', 'photo']
    
    # Optionally, you can add search and filter options
    search_fields = ['user__username', 'email']
    list_filter = ['user']


# Registering the models separately
admin.site.register(Recipe)  # Registering the Recipe model
admin.site.register(Profile, ProfileAdmin)  # Registering the Profile model with the custom admin class

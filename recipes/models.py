from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')  # to associate recipes with a user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    # Add any other fields you need for a profile

    def __str__(self):
        return f'{self.user.username} Profile'



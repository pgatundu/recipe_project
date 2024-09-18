from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    # Add any other fields you need for a profile

    def __str__(self):
        return f'{self.user.username} Profile'

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title

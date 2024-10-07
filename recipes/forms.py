from django import forms
from .models import Recipe, Profile, FoodPhoto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'description', 'instructions','food_photo']
        widgets = {
            'photo': forms.FileInput(attrs={'required': True}),
        }

class FoodPhotoForm(forms.ModelForm):
    class Meta:
        model = FoodPhoto
        fields = ['image']

FoodPhotoFormSet = modelformset_factory(FoodPhoto, form=FoodPhotoForm, extra=4, max_num=4)       

        

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'photo','email'] 
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }


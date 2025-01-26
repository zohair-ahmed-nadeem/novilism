from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
import os

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomRegisterForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def process_image(self, image):
        if image:
            img = Image.open(image)
            img = img.convert('RGB')
            # Resize to 2x2
            img.thumbnail((2, 2), Image.Resampling.LANCZOS)
            # Save processed image
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            return buffer.getvalue()
        return None

    def save(self, commit=True):
        user = super().save(commit=False)  # Don't commit yet
        if commit:
            user.save()  # This will trigger profile creation via signal
            
            # Get or create the profile instead of assuming it exists
            from post.models import Profile
            profile, created = Profile.objects.get_or_create(user=user)
            
            if self.cleaned_data.get('profile_picture'):
                processed_image = self.process_image(self.cleaned_data['profile_picture'])
                if processed_image:
                    profile.profile_picture.save(
                        f'{user.username}_profile.jpg',
                        BytesIO(processed_image),
                        save=True
                    )
        return user
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Username is required.")
        if not username.isalnum() and not all(char in '@./+/-/_' for char in username):
            raise forms.ValidationError("Username must contain only letters, digits, and @/./+/-/_ characters.")
        return username
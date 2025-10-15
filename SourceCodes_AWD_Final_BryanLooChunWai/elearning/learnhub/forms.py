# import libraries and modules
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LearnHubUser, Course, Material
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import LearnHubUser
from .models import Course

# define validators functions to ensure data integrity and reliability
def validate_username(value):
    if not value.isalnum():
        raise ValidationError("Username should only contain letters and numbers.")

def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in value):
        raise ValidationError("Password must contain at least one digit.")
    if not any(char.isalpha() for char in value):
        raise ValidationError("Password must contain at least one letter.")

# define form class for the different pages
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        validators=[validate_username],
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        required=True
    )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    is_student = forms.BooleanField(required=False)
    is_teacher = forms.BooleanField(required=False)
    profile_picture = forms.ImageField(required=False)
    organisation = forms.CharField(max_length=256, required=False)
    
    username = forms.CharField(
        max_length=150, 
        required=True, 
        validators=[validate_username]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validate_password_strength]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validate_password_strength]
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def clean_email(self):
        """ Ensure the email is unique. """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            LearnHubUser.objects.create(
                user=user,
                is_student=self.cleaned_data.get("is_student", False),
                is_teacher=self.cleaned_data.get("is_teacher", False),
                profile_picture=self.cleaned_data.get("profile_picture", None),
                organisation=self.cleaned_data.get("organisation", "")
            )
        return user

class CourseForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        error_messages={"required": "Course name is required."}
    )
    description = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        error_messages={"min_length": "Description should be at least 10 characters long."}
    )

    class Meta:
        model = Course
        fields = ["name", "description"]


ALLOWED_FILE_TYPES = ["pdf", "docx", "pptx", "txt", "jpg", "png", "mp4", "zip"]

def validate_file_extension(value):
    """ Ensure uploaded file is of an allowed type. """
    ext = value.name.split(".")[-1].lower()
    if ext not in ALLOWED_FILE_TYPES:
        raise ValidationError(f"Invalid file type. Allowed formats: {', '.join(ALLOWED_FILE_TYPES)}")

class MaterialForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(validators=[validate_file_extension])

    class Meta:
        model = Material
        fields = ["title", "description", "file"]

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['content', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False

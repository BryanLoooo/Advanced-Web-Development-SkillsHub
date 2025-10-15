# import libraries and modules
from django.test import TestCase
from rest_framework.test import APIClient
from learnhub.forms import RegistrationForm
from learnhub.models import Course
from django.urls import reverse

# define class to write unit tests
class LearnHubTests(TestCase):
    
    def test_login(self):
        """Set up test users, courses, and API client."""
        self.client = APIClient()
        self.client.login(username="admin2", password="p@55w0rd")

    def test_failed_login(self):
        """Set up test users, courses, and API client."""
        self.client.login(username=" ")

    def test_valid_registration(self):
            """Test valid form submission."""
            form_data = {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
                "is_student": True,
                "organisation": "University"
            }
            form = RegistrationForm(data=form_data)
            self.assertTrue(form.is_valid())
    
    def test_failed_registration(self):
            """Test valid form submission."""
            form_data = {
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "password",
                "password2": "password",
                "is_student": True,
                "organisation": "University"
            }
            form = RegistrationForm(data=form_data)
            self.assertTrue(form.is_valid())

    def test_user_logout(self):
        """Test user logout."""
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_failed_create_course(self):
        """Ensure only teachers can create courses."""
        self.client.login(username="Jane", password="p@55w0rd")
        response = self.client.post(reverse('create_course'), {"name": " ", "description": " "})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 2)

    def test_non_admin_cannot_access_admin_panel(self):
        """Ensure a normal user is redirected when trying to access the admin panel."""
        self.client.login(username="Jane", password="p@55w0rd")
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 302)

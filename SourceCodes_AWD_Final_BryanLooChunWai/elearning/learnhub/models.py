# import libraries and modules
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User

# define classes for the different models to store data for storage
class LearnHubUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="learnhub_users")
    user_permissions = models.ManyToManyField(Permission, related_name="learnhub_user_permissions")
    organisation = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."
    
class StatusUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="status_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field for read status

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

class Alert(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notifications')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"
    
class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in {self.room_name}: {self.message[:50]}"
    
class EnrollmentNotification(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollment_notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"

class ResourceNotification(models.Model):
    resource = models.ForeignKey(Material, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"New resource '{self.resource.title}' for {self.student.username}"
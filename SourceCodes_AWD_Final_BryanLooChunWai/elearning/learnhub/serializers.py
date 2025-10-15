# import libraries and modules
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Material, Feedback, ChatMessage

# define new serializer classes
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class CourseSerializer(serializers.ModelSerializer):
    
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "description", "teacher", "students"]
        extra_kwargs = {"students": {"read_only": True}}

class CourseDetailSerializer(serializers.ModelSerializer):

    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "description", "teacher", "students", "materials"]

    def get_materials(self, obj):
        return MaterialSerializer(obj.materials.all(), many=True).data

class MaterialSerializer(serializers.ModelSerializer):

    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Material
        fields = ["id", "course", "title", "description", "file", "uploaded_at"]

class FeedbackSerializer(serializers.ModelSerializer):

    student = UserSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Feedback
        fields = ["id", "student", "course", "comment", "created_at"]

class ChatMessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "room_name", "sender", "message", "timestamp"]

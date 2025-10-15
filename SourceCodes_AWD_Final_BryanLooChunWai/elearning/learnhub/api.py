# import libraries and modules
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Course, Material, Feedback, ChatMessage
from .serializers import (
    UserSerializer,
    CourseSerializer,
    CourseDetailSerializer,
    FeedbackSerializer,
    MaterialSerializer,
    ChatMessageSerializer,
)

# define class for retrieving and sending information
class CourseListViewAPI(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.learnhubuser.is_teacher:
            return Response({"error": "Only teachers can create courses."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(teacher=self.request.user)

class CourseDetailViewAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        if request.user != course.teacher:
            return Response({"error": "Only the course teacher can update this course."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        course = self.get_object()
        if request.user != course.teacher:
            return Response({"error": "Only the course teacher can delete this course."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class JoinCourseViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if request.user in course.students.all():
            return Response({"message": "Already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)
        course.students.add(request.user)
        return Response({"message": "Successfully joined the course."}, status=status.HTTP_200_OK)

class AddMaterialViewAPI(generics.CreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        if self.request.user != course.teacher:
            return Response({"error": "Only the course teacher can add materials."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(course=course)

class UserListViewAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailViewAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedbackViewAPI(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.learnhubuser.is_student:
            return Response({"error": "Only students can submit feedback."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(student=self.request.user)

class ChatMessageListViewAPI(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        return ChatMessage.objects.filter(room_name=room_name).order_by("timestamp")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

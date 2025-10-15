# import libraries and modules
from django.urls import path
from .views import AdminPanelView, ChatView, ProfileView, CourseDetailView, FeedbackView, BrowseProfilesView, UserDetailView
from .views import CourseCreateView, CourseListView, MarkEnrollmentAsReadView, MarkResourceAsReadView, DeleteStudentView
from .views import AdminPanelView, HomePageView, UpdateListView, AddMaterialView, MarkAsReadView
from .views import register, user_login, user_logout, join_course
from django.contrib.auth.decorators import login_required
from . import views
from .api import (
    CourseListViewAPI,
    CourseDetailViewAPI,
    AddMaterialViewAPI,
    UserListViewAPI,
    UserDetailViewAPI,
    FeedbackViewAPI,
    ChatMessageListViewAPI
)

urlpatterns = [
    # urls for registration, login and logout
    path('learnhub/register/', register, name='register'),
    path('learnhub/login/', user_login, name='login'),
    path('learnhub/logout/', user_logout, name='logout'),

    # urls for home page
    path('learnhub/home/', login_required(login_url='login')(HomePageView.as_view()), name='home'),

    # urls for live chat rooms
    path('learnhub/chat/', login_required(login_url='login')(ChatView.as_view()), name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),

    # urls for profile related pages
    path('learnhub/profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('learnhub/user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('learnhub/browse_profiles/', login_required(login_url='login')(BrowseProfilesView.as_view()), name='browse_profiles'),

    # urls for course related pages
    path('courses/<int:course_id>/join/', join_course, name='join_course'),
    path('learnhub/courses/<int:pk>/', login_required(login_url='login')(CourseDetailView.as_view()), name='course_detail'),
    path('learnhub/courses/', login_required(login_url='login')(CourseListView.as_view()), name='courses'),
    path('learnhub/create_course/', login_required(login_url='login')(CourseCreateView.as_view()), name='create_course'),

    # urls for feedback page
    path('learnhub/feedback/', login_required(login_url='login')(FeedbackView.as_view()), name='feedback'),
    
    # urls for user account management
    path('admin_panel/', login_required(login_url='login')(AdminPanelView.as_view()), name='admin_panel'),
    path('admin_panel/delete/<int:pk>/', login_required(login_url='login')(DeleteStudentView.as_view()), name='delete_student'),

    # urls for update related pages
    path('updates/', UpdateListView.as_view(), name='updates'),
    path("update/read/<int:update_id>/", MarkAsReadView.as_view(), name="mark_as_read"),

    # urls for enrolment related pages
    path('learnhub/courses/<int:course_id>/add_material/', AddMaterialView.as_view(), name='add_material'),

    # urls for marking successful enrolment into a course
    path("enrollment/read/<int:notification_id>/", MarkEnrollmentAsReadView.as_view(), name="mark_enrollment_as_read"),

    # urls for marking newly uploaded resources as read
    path("resource/read/<int:notification_id>/", MarkResourceAsReadView.as_view(), name="mark_resource_as_read"),


    # API endpoints for Courses
    path('api/courses/', CourseListViewAPI.as_view(), name='api_courses'),
    path('api/courses/<int:pk>/', CourseDetailViewAPI.as_view(), name='api_course_detail'),

    # API endpoints for Users
    path('api/users/', UserListViewAPI.as_view(), name='api_users'),
    path('api/users/<int:pk>/', UserDetailViewAPI.as_view(), name='api_user_detail'),

    # API endpoints for Feedback
    path('api/learnhub/feedback/', FeedbackViewAPI.as_view(), name='api_feedback'),

    #e API endpoints for AddMaterial
    path('api/learnhub/courses/<int:course_id>/add_material/', AddMaterialViewAPI.as_view(), name='api_add_material'),

    # API endpoints for Chat message list
    path('api/learnhub/chat/<str:room_name>/', ChatMessageListViewAPI.as_view(), name='api_chat_message_list'),
]
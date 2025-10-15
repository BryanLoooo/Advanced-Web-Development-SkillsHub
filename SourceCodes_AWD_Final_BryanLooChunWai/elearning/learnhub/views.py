# import libraries and modules
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DeleteView, FormView, TemplateView, DetailView
from django.views import View
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, MaterialForm, StatusUpdateForm, CourseForm
from .models import LearnHubUser, StatusUpdate, ChatMessage, Alert, Course, EnrollmentNotification, ResourceNotification, User, Course, Feedback

# user authentication views
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/learnhub/home/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    return render(request, 'learnhub/login.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            registered = True
            return redirect('login')
        else:
            print(user_form.errors)
    else:
        user_form = RegistrationForm()
    return render(request, 'learnhub/register.html', {
        'registration_form': user_form,
        'registered': registered
    })

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/learnhub/login/')
    
# home page view
class HomePageView(FormView):
    template_name = "learnhub/home.html"
    form_class = StatusUpdateForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            status = form.save(commit=False)
            status.user = self.request.user
            status.save()
            messages.success(self.request, "Your status update has been posted successfully!")
            return redirect("home")
        else:
            return redirect("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["updates"] = StatusUpdate.objects.filter(read=False)

        if self.request.user.is_authenticated and self.request.user.learnhubuser.is_teacher:
            context["enrollment_notifications"] = EnrollmentNotification.objects.filter(
                teacher=self.request.user, read=False
            )
        elif self.request.user.learnhubuser.is_student:
            context["resource_notifications"] = ResourceNotification.objects.filter(
                student=self.request.user, read=False
            )
        else:
            context["enrollment_notifications"] = []
            context["resource_notifications"] = []
        return context
    
# live chat views
class ChatView(ListView):
    model = ChatMessage
    template_name = "learnhub/chat.html"
    context_object_name = 'chatMessage'

def room(request, room_name):
    messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')[:50]
    return render(request, 'learnhub/room.html', {'room_name': room_name, 'messages': messages})

# profile related views
class ProfileView(TemplateView):
    template_name = "learnhub/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        context["profile_user"] = get_object_or_404(LearnHubUser, user__username=username)
        return context
    
class BrowseProfilesView(TemplateView):
    template_name = "learnhub/browse_profiles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        if query:
            users = User.objects.filter(username__icontains=query)
        else:
            users = User.objects.all()
        context['users'] = users
        context['query'] = query
        return context

class UserDetailView(DetailView):
    model = User
    template_name = "learnhub/user_detail.html"
    context_object_name = "user_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["learnhub_user"] = self.object.learnhubuser
        except LearnHubUser.DoesNotExist:
            context["learnhub_user"] = None
        return context

# course related views
class CourseCreateView(TemplateView):
    template_name = "learnhub/create_course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            print("Course created successfully!")
            return redirect("courses")

        print("Error: Unable to create course!")
        return self.render_to_response({"form": form})
    
class CourseListView(ListView):
    model = Course
    template_name = 'learnhub/courses.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'learnhub/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        return context

def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user in course.students.all():
        messages.info(request, "You are already enrolled in this course.")
    else:
        course.students.add(request.user)
        messages.success(request, "Successfully joined the course!")
        EnrollmentNotification.objects.create(
            course=course,
            student=request.user,
            teacher=course.teacher
        )
    return redirect('course_detail', pk=course_id)

class AddMaterialView(View):
    template_name = "learnhub/add_material.html"

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=self.kwargs["course_id"])
        if request.user != self.course.teacher:
            messages.error(request, "You are not authorized to add materials to this course.")
            return redirect("course_detail", course_id=self.course.id)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = MaterialForm()
        return render(request, self.template_name, {"form": form, "course": self.course})

    def post(self, request, *args, **kwargs):
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = self.course
            material.save()

            for student in self.course.students.all():
                ResourceNotification.objects.create(resource=material, student=student)

            messages.success(request, "Resource added successfully!")
            return redirect(reverse("course_detail", kwargs={"pk": self.course.id}))
        return render(request, self.template_name, {"form": form, "course": self.course})

# user management views
class AdminPanelView(ListView):
    model = User
    template_name = "learnhub/admin_panel.html"
    context_object_name = "students"

    def get_queryset(self):
        return User.objects.filter(learnhubuser__is_student=True)

class DeleteStudentView(DeleteView):
    model = User
    template_name = "learnhub/confirm_delete.html"
    success_url = reverse_lazy("admin_panel")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Student deleted successfully.")
        return super().delete(request, *args, **kwargs)

# mark as read views to update list of notifications
class MarkAsReadView(View):
    def post(self, request, update_id):
        update = get_object_or_404(StatusUpdate, id=update_id)
        update.read = True
        update.save()
        messages.success(request, "Update marked as read!")
        return HttpResponseRedirect(reverse("updates"))
    
class MarkEnrollmentAsReadView(View):
    def post(self, request, notification_id):
        notification = get_object_or_404(EnrollmentNotification, id=notification_id)
        if request.user == notification.teacher:
            notification.read = True
            notification.save()
        return HttpResponseRedirect(reverse("home"))
    
class MarkResourceAsReadView(View):
    def post(self, request, notification_id):
        notification = get_object_or_404(ResourceNotification, id=notification_id)
        if request.user == notification.student:
            notification.read = True
            notification.save()
        return HttpResponseRedirect(reverse("home"))
    
# feeback related views
class FeedbackView(TemplateView):
    template_name = 'learnhub/feedback.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Ensure the user is a student
        if not hasattr(user, 'learnhubuser'):
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["courses"] = user.enrolled_courses.all()
        context["feedbacks"] = Feedback.objects.filter(student=user)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        courses = user.enrolled_courses.all()
        course_id = request.POST.get("course")
        comment = request.POST.get("comment")
        if course_id and comment:
            try:
                course = Course.objects.get(id=course_id)
                if course in courses:
                    Feedback.objects.create(course=course, student=user, comment=comment)
                    messages.success(request, "Feedback submitted successfully!")
            except Course.DoesNotExist:
                messages.error(request, "Invalid course selection.")
        return redirect("feedback")
    
# updates page view    
class UpdateListView(ListView):
    model = StatusUpdate
    template_name = "learnhub/updates.html"
    context_object_name = "updates"
    ordering = ["-created_at"]
# 🎓 E-Learning Web Application

An advanced Django-based E-learning platform designed to provide secure, scalable, and interactive online education for both students and teachers.  
Built with **Django**, **Django REST Framework**, **WebSockets**, **Celery**, and **Redis**, the application enables real-time communication, course management, and robust authentication.

---

## 🚀 Features

| Category | Description |
|-----------|--------------|
| **Authentication** | Secure login and registration using Django’s authentication framework with role-based access control (RBAC). |
| **Course Management** | Teachers can create, edit, and manage courses; students can enroll and access uploaded materials. |
| **Real-Time Chat** | WebSocket-powered live chat between students and teachers via Django Channels. |
| **Notifications** | Automated alerts for new enrollments and resource uploads using Celery and Redis. |
| **Feedback System** | Students can submit feedback; teachers receive notifications instantly. |
| **RESTful API** | Django REST Framework (DRF) ensures seamless communication between frontend and backend. |
| **Testing & Security** | Comprehensive unit tests, HTTPS, CSRF protection, and password validators implemented. |

---

## 🧩 System Architecture

The platform follows the **Model-View-Controller (MVC)** pattern for maintainability and scalability.

**Stack Overview:**
- **Frontend:** Django Templates + Bootstrap 5  
- **Backend:** Django + Django REST Framework  
- **Database:** SQLite  
- **Real-Time Engine:** Django Channels (WebSockets)  
- **Task Queue:** Celery with Redis  
- **Hosting:** Configured for local deployment; compatible with AWS or cloud servers.

---

## 🧱 Database Entities

- **User / LearnHubUser:** Handles role-based profiles (student or teacher).  
- **Course & Material:** Manage course creation and resource uploads.  
- **Feedback:** Stores user feedback and timestamps.  
- **ChatMessage:** Handles real-time user communications.  
- **Notifications:** Tracks new enrollments and material updates.

---

## 🧠 Core API Endpoints

| Endpoint | Function |
|-----------|-----------|
| `/api/users/` | Retrieve and manage user details |
| `/api/courses/` | Browse and enroll in courses |
| `/api/feedback/` | Submit and fetch course feedback |

All endpoints use **JSON** format and follow **RESTful** principles for scalability.

---

## ⚙️ Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/elearning-webapp.git
cd elearning-webapp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Start Redis and Celery
redis-server
celery -A elearning worker -l info

# 5. Run the server
python manage.py runserver

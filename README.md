# 🚀 Django CRM System

A full-stack Customer Relationship Management (CRM) system built with Django, PostgreSQL, Bootstrap, and CKEditor.

<p align="center">
  <img src="assets/dashboard.png" width="900">
</p>

---

## 🌐 Live Demo

🔗 https://django-crm-system-yegs.onrender.com

---

## ✨ Features

### 👥 Role Based Access Control

| Role | Permissions |
|--------|------------|
| Admin | Full system access |
| Manager | Manage companies, employees, and tasks |
| Employee | View assigned tasks and update status |

---

### 🏢 Company Management

- Create Companies
- Update Company Information
- Company Logo Upload
- Search Companies
- Pagination Support

---

### 👨‍💼 Employee Management

- Create Employees
- Assign Employees to Companies
- Upload Profile Images
- Employee Detail Pages
- CRUD Operations

---

### 📋 Task Management

- Create Tasks
- Assign Tasks to Employees
- Task Priorities
- Task Status Tracking
- Task Attachments
- Rich Text Descriptions using CKEditor

---

### 📊 Dashboard

- Total Companies
- Total Employees
- Total Tasks
- Recent Tasks Overview
- Role-Based Dashboard Content

---

### 🔐 Authentication & Authorization

- Login System
- Logout System
- Protected Routes
- Custom Permission Decorators
- Group-Based Access Control

---

### ⚠️ Error Handling

- Custom 403 Page
- Custom 404 Page
- Form Validation
- Permission Checks

---

## 🛠️ Tech Stack

### Backend

- Django 6
- PostgreSQL
- Django ORM

### Frontend

- HTML5
- CSS3
- Bootstrap 5

### Additional Packages

- CKEditor
- Pillow
- WhiteNoise
- Gunicorn
- python-dotenv

### Deployment

- Render
- PostgreSQL Database
- GitHub Integration

---

## 🗄️ Database Design

```text
Company
   │
   └── Employee
            │
            └── Task
```

### Models

#### Company

- Name
- Email
- Phone
- Address
- Logo

#### Employee

- User
- Company
- Designation
- Phone
- Profile Image

#### Task

- Title
- Description
- Employee
- Status
- Priority
- Deadline
- Attachment

---

## 📸 Screenshots

### Dashboard

![Dashboard](assets/dashboard.png)

### Companies

![Companies](assets/company.png)

### Employees

![Employees](assets/employee.png)

### Tasks

![Tasks](assets/task.png)

### CKEditor Integration

![CKEditor](assets/ckeditor.png)

---

## 🔄 System Workflow

```text
Admin
   │
   ├── Creates Companies
   │
   ├── Creates Employees
   │
   └── Assigns Tasks
            │
            ▼
        Employee
            │
            ▼
     Updates Task Status
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/django-crm-system.git
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Environment

```bash
env\Scripts\activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

---

## 📦 Deployment

The project is deployed using:

- Render Web Service
- PostgreSQL Database
- WhiteNoise Static Files
- GitHub Auto Deploy

Every push to the main branch automatically triggers a redeployment.

---

## 🎯 Learning Outcomes

This project demonstrates:

- Django Authentication
- Django Authorization
- Custom Decorators
- CRUD Operations
- PostgreSQL Integration
- File Upload Handling
- CKEditor Integration
- Environment Variables
- Production Deployment
- Git & GitHub Workflow
- Render Deployment

---

## 👨‍💻 Author

**Shaurya Vrat Shukla**

Python Developer | Django Developer | AI/ML Enthusiast

GitHub: https://github.com/Shaurya-thinker

LinkedIn: https://www.linkedin.com/in/shaurya-vrat-shukla/

---
⭐ If you found this project useful, consider giving it a star.
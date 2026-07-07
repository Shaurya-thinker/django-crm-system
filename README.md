# <p align="center">🚀 Django CRM System</p>

<p align="center">
  <b>Role-based CRM platform built with Django, PostgreSQL, CKEditor, and Cloudinary</b>
</p>

<p align="center">

![Django](https://img.shields.io/badge/Django-6.0-green?style=for-the-badge\&logo=django)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge\&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge\&logo=postgresql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge\&logo=bootstrap)
![Render](https://img.shields.io/badge/Hosted%20On-Render-black?style=for-the-badge\&logo=render)

</p>

---

# 🌐 Live Demo

Production URL: [django-crm-system-yegs.onrender.com](https://django-crm-system-yegs.onrender.com)

---

# 🎮 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `demo_admin` | `demo@1234` |
| Manager | `demo_manager` | `demo@1234` |
| Representative | `demo_representative` | `demo@1234` |

> Demo accounts are intended for evaluation. Admin features are controlled through role and permission checks in the app.

---

# 📖 Project Overview

Django CRM System is a customer relationship management application for managing companies, employees, tasks, and role-based access. The app now includes a dedicated access control module, CSV company import/export helpers, email notifications, Cloudinary-backed media uploads, and dynamic AJAX-driven form behavior.

The project demonstrates real-world Django concepts including:

* Authentication and authorization
* Custom role and permission management
* Company, employee, and task workflows
* Search, filtering, and pagination
* Rich text task descriptions with CKEditor
* File uploads for logos, profiles, and task attachments
* CSV import/export and template download
* Email notifications for key workflow events
* Environment-based configuration
* Production deployment with Render

---

# ⭐ Highlights

* Role-Based Access Control (RBAC)
* Dynamic Manager–Representative hierarchy
* Company & Task assignment workflows
* CKEditor rich text editor
* Cloudinary media storage
* AJAX-powered dynamic forms
* CSV import/export support
* Email notification system
* Responsive Bootstrap UI
* Production deployment on Render

---

# ✨ Core Features

### 🛡 Access Control

* Admin-only access role management
* Role-permission mapping through `Role`, `Permission`, and `RolePermission`
* Permission checks for company, employee, task, and import actions
* Custom 403 and 404 error pages

### 🏢 Company Management

* Create, update, and delete companies
* Slug-based company URLs
* Company logo uploads
* Search and pagination
* CSV import, export, and template download
* Manager and representative assignment rules

### 👨‍💼 Employee Management

* Create, update, and delete employees
* User account creation during employee onboarding
* Profile image uploads
* Reporting manager assignment
* Access role assignment and filtering
* Validation for username, email, and phone number uniqueness

### 📋 Task Management

* Create, update, and delete tasks
* Assign tasks to representatives
* Priority and status tracking
* Deadlines and file attachments
* CKEditor-rich task descriptions
* Manager-scoped task assignment rules

### 📊 Dashboard and Profile

* Role-aware dashboard counts
* Recent task summaries
* Representative company listing
* Personal profile page for logged-in users

### 🔔 Workflow Automation

* Welcome emails for newly created employees
* Task assignment notifications
* Task reassignment notifications
* Company assignment notifications
* Company reassignment notifications
* Password reset via Django Authentication
* AJAX endpoints for dynamic dropdowns and validation

### 📧 Email Notifications

The system automatically sends email notifications for important workflow events:

* Welcome email when a new employee account is created
* Task assignment notifications
* Task reassignment notifications
* Company assignment notifications
* Company reassignment notifications
* Password reset emails (Django Authentication)

---

# 📈 Project Statistics

| Metric | Value |
| ------ | ----- |
| Core Models | 6 |
| Main Modules | Company, Employee, Task, Access Control |
| User Roles | Admin, Manager, Representative |
| Database | PostgreSQL |
| Authentication | Django Auth |
| Rich Text Editor | CKEditor |
| Media Storage | Cloudinary |
| Deployment | Render |
| Version Control | Git + GitHub |

---

# 🏗 System Architecture

```text
Browser
   │
   ▼
Render
   │
   ▼
Gunicorn
   │
   ▼
Django Application
   │
   ├── Django ORM
   ├── CKEditor
   ├── SMTP Email
   └── Cloudinary Media Storage
   │
   ▼
PostgreSQL Database
```

---

# 🔄 Application Workflow

```text
Admin
   │
   ├── Creates access roles and permissions
   ├── Creates companies
   ├── Creates employees
   └── Assigns tasks
            │
            ▼
Manager
   │
   ├── Manages assigned companies
   ├── Manages representatives
   └── Assigns tasks to team members
            │
            ▼
Representative
   │
   └── Views assigned companies and tasks
```

---

# 🗄 Data Model

```text
Role ──< RolePermission >── Permission
  │
  ▼
Employee ──< Company
  │            │
  │            └──< Task
  └── Reporting Manager (self reference)
```

---

# 📸 Application Preview

## Dashboard

![Dashboard](assets/dashboard.png)

## Companies Module

![Companies](assets/company.png)

## Employees Module

![Employees](assets/employee.png)

## Tasks Module

![Tasks](assets/task.png)

## CKEditor Integration

![CKEditor](assets/ckeditor.png)

---

# 🛠 Technology Stack

## Backend

* Python 3.13
* Django 6.0.5

## Database

* PostgreSQL

## Frontend

* HTML5
* CSS3
* Bootstrap 5.3
* JavaScript (AJAX)
* Django Templates

## Packages

* django-ckeditor
* django-cloudinary-storage
* cloudinary
* Pillow
* psycopg2-binary
* python-dotenv
* WhiteNoise
* Gunicorn

## Integrations

* SMTP email notifications
* Cloudinary media storage

## Deployment

* Render
* GitHub
* PostgreSQL

---

# 📂 Project Structure

```text
crm_project/
│
├── crm/
│   ├── migrations/
│   ├── templates/
│   │   ├── emails/
│   │   └── ...
│   ├── templatetags/
│   ├── forms.py
│   ├── models.py
│   ├── utils.py
│   ├── views.py
│   └── urls.py
│
├── crm_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── assets/
├── media/
├── static/
├── requirements.txt
├── Procfile
├── manage.py
└── README.md
```

---

# 🚀 Installation Guide

## Clone Repository

```bash
git clone https://github.com/Shaurya-thinker/django-crm-system.git
cd django-crm-system
```

## Create Virtual Environment

```bash
python -m venv env
```

## Activate Environment

### Windows

```bash
env\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Run Development Server

```bash
python manage.py runserver
```

---

# 🌍 Deployment

The application is deployed using:

* Render Web Service
* PostgreSQL Database
* WhiteNoise Static Files
* Gunicorn WSGI Server
* Cloudinary Media Storage
* GitHub Auto Deploy

### CI/CD Flow

```text
Code Changes
      │
      ▼
Git Push
      │
      ▼
GitHub Repository
      │
      ▼
Render Auto Deploy
      │
      ▼
Production Website
```

---

# 🎯 Key Concepts Demonstrated

### Django

* Models
* Views
* Templates
* Forms
* Authentication
* Authorization
* Custom Decorators

### Database

* PostgreSQL
* ORM Relationships
* Migrations

### Production

* Environment Variables
* Static Files
* WhiteNoise
* Gunicorn
* Render Deployment

### Software Engineering

* Git
* GitHub
* CI/CD
* Documentation
* Project Structuring

---

# 🚀 Future Enhancements

* REST API using Django REST Framework
* Activity Logs / Audit Trail
* Docker Support
* AWS Deployment
* Analytics Dashboard
* In-app Notification Center
* Real-time Notifications (WebSockets)
* Two-Factor Authentication

---

# 📚 Learning Outcomes

This project helped me gain hands-on experience with:

* Django Authentication & Authorization
* Role-Based Access Control (RBAC)
* PostgreSQL Database Design
* CKEditor Integration
* Cloudinary Media Storage
* AJAX-based Dynamic Forms
* Email Notifications using SMTP
* CSV Import & Export
* CRUD Operations
* File Upload Handling
* Django Template Tags
* Production Deployment on Render
* Git & GitHub Workflow
* Environment Variables
* CI/CD Concepts

---

## 👨‍💻 Author

**Shaurya Vrat Shukla**

Backend Developer | Django Developer | Python Enthusiast

GitHub: https://github.com/Shaurya-thinker

LinkedIn: https://www.linkedin.com/in/shaurya-vrat-shukla


---

<p align="center">
⭐ If you found this project interesting, consider giving it a star.
</p>




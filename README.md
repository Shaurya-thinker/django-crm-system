# Django CRM System

A role-based Customer Relationship Management (CRM) system built with Django and PostgreSQL. This project was developed as part of a Django learning internship to explore real-world web development concepts such as authentication, authorization, CRUD operations, file uploads, search, filtering, role management, and PostgreSQL integration.

---

## Features

### Authentication & Authorization

* User Login and Logout
* Protected Routes using Django Authentication
* Role-Based Access Control using Django Groups

### Roles

#### Admin

* Full access to the system
* Manage companies, employees, and tasks

#### Manager

* Manage companies and tasks
* View organizational data

#### Employee

* View only assigned tasks
* Personalized dashboard experience

---

## Dashboard

* Total Companies Count
* Total Employees Count
* Total Tasks Count
* Recent Tasks Overview
* Role-aware task visibility

---

## Company Management

* Create Company
* View Company Details
* Update Company Information
* Delete Company
* Company Logo Upload
* Search Companies
* Pagination
* SEO-friendly Slug URLs

---

## Employee Management

* Create Employee
* View Employee Details
* Update Employee Information
* Delete Employee
* Employee Profile Image Upload
* Search Employees
* Pagination

---

## Task Management

* Create Tasks
* Assign Tasks to Employees
* Update Tasks
* Delete Tasks
* Task Status Tracking
* Task Priority Management
* Task Attachments
* Deadline Management
* Task Detail View

### Task Status

* Pending
* In Progress
* Completed

### Task Priority

* Low
* Medium
* High

---

## Search & Filtering

### Company Search

Search companies by name.

### Employee Search

Search employees by username.

### Task Search

Search tasks by title.

### Task Filters

* Filter by Status
* Filter by Priority

---

## Rich Text Editing

Integrated CKEditor for task descriptions to support:

* Rich Text Formatting
* Lists
* Headings
* Links
* Enhanced Content Editing

---

## Error Handling

* Custom 403 Forbidden Page
* Custom 404 Not Found Page
* Form Validation
* Permission-Based Access Control

---

## Database Design

### Company

* Name
* Email
* Phone
* Address
* Logo

### Employee

* User
* Company
* Designation
* Profile Image

### Task

* Title
* Description
* Employee
* Status
* Priority
* Deadline
* Attachment
* Created At

---

## Technologies Used

### Backend

* Django 6
* Python 3

### Database

* PostgreSQL

### Frontend

* HTML
* Bootstrap 5
* Django Templates

### Additional Packages

* django-ckeditor
* pillow
* psycopg2-binary
* python-dotenv

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd django-crm-system
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Virtual Environment

Windows:

```bash
env\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Run Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

---

## Learning Outcomes

This project helped explore:

* Django Models
* Django ORM
* CRUD Operations
* Authentication
* Authorization
* Django Groups and Permissions
* Model Forms
* File Uploads
* Pagination
* Search and Filtering
* PostgreSQL Integration
* Environment Variables
* Third-Party Package Integration
* Template Inheritance
* Custom Template Tags
* Role-Based Access Control

---

## Future Enhancements

* Deployment on Cloud Platform
* Automated CI/CD Pipeline
* Docker Containerization
* REST API using Django REST Framework
* Email Notifications
* Activity Logs
* Advanced Reporting Dashboard

---

## Author

**Shaurya Vrat Shukla**

Built as part of a Django Internship Learning Project to gain hands-on experience with full-stack web application development using Django and PostgreSQL.

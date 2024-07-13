# 📚 Course Management System

Welcome to the Course Management System, a robust platform designed to streamline the management of educational courses and user roles. Built with FastAPI, SQLAlchemy, and PostgreSQL, this system supports user authentication, role-based access control, and comprehensive CRUD operations for courses and sections.

## 🚀 Features

- **User Registration & Authentication**: Secure user management with unique email addresses.
- **Role-Based Access Control**: Differentiates between teacher and student functionalities.
- **Course & Section Management**: Complete CRUD operations for courses and sections.
- **Profile Management**: Personalize user profiles with biographical information.
- **Database Migrations**: Seamless database updates with Alembic.

## 🗂️ Project Structure


## 🛠️ Setup and Installation

### Prerequisites

- **Python 3.12**
- **PostgreSQL**
- **Poetry**

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone git@github.com:hasnain-hasib/course_management.git
   cd course_management

Demo : 

curl -X 'POST' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "example@example.com",
  "password": "string",
  "role": 1
}'

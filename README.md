# Task Management Application - Svelte + Django REST

## Author

- **Alesia Hajrulla**

_All development was completed independently._

---

## Project Overview

This full-stack application allows users to manage tasks with a simple and intuitive interface. It supports:

- Adding, editing, and deleting tasks
- Searching and filtering tasks
- Paginated view for better UX
- User authentication with login, logout, and signup functionality

The backend is built using **Django REST Framework**, while the frontend uses **Svelte** with **Tailwind CSS**.

---

## Functionalities

- Create a task
- Edit or delete an existing task
- Filter by status (All, To Do, Done)
- Search by task title
- View tasks across pages with pagination
- **User Authentication**:
  - **Login**: Users can log in with email and password
  - **Signup**: Users can create a new account
  - **Logout**: Users can log out and be redirected to the login page

---

## Backend: Django REST

- API developed with Django 5.2 and Django REST Framework
- SQLite3 used as local database
- CORS enabled to allow frontend access
- Pagination implemented using `PageNumberPagination`

### How to Run (Backend)

```bash
cd taskmanager
python3 -m venv venvv
source venvv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API base URL: `http://localhost:8000/api/tasks/`  
Custom search endpoint: `http://localhost:8000/api/tasks/search/` (POST)

---

## Frontend: Svelte + Tailwind CSS

- User-friendly interface using Svelte
- Live search and dropdown filter
- Modal form for task creation/editing
- Pagination component fixed at the bottom
- User authentication with login, logout, and signup forms

### How to Run (Frontend)

```bash
cd task-frontend
npm install
npm run dev
```

App will run at: `http://localhost:5173/`

The backend is running at `localhost:8000`.

---

## Code Structure

```
project-root/
│
├── taskmanager/              # Backend Django API
│   ├── tasks/                # Django app (models, views, serializers)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── users/                 # Django app for user-related functionalities
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── db.sqlite3            # Local SQLite database
│   ├── manage.py
│   └── requirements.txt
│
└── task-frontend/            # Frontend Svelte app
    ├── src/                  # Source code
    │   ├── assets/           # Static assets
    │   ├── components/       # TaskTable.svelte, TaskForm.svelte
    │   ├── pages/            # Dashboard, Login, Signup components
    │   │   ├── dashboard.svelte
    │   │   ├── login.svelte
    │   │   └── signup.svelte
    │   ├── stores.js         # Svelte store for tasks and user authentication
    │   ├── app.css           # Tailwind CSS customizations
    │   ├── App.svelte        # Main application UI
    │   └── main.js
    ├── public/                # Public assets (e.g., index.html)
    ├── node_modules/          # Node.js modules
    ├── package.json
    └── vite-env.d.ts         # TypeScript environment configuration
```

---

## Notes

- You can reset the database anytime using:

```bash
rm db.sqlite3
python manage.py migrate
```

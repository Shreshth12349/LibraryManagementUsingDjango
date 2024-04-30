# Library Management System - Django Project

Welcome to the Library Management System Django project! This system provides a platform for managing library operations including issuing and returning books, maintaining student records, and logging book transactions.

## Features

- **Authentication**: Users can register and login to the system.
- **Home**: Dashboard providing an overview of the library system.
- **View Students**: View and manage student records.
- **Search Students**: Search for students by name, registration number, or department.
- **Search Books**: Search for books by title, author, description, or availability status.
- **Select Book**: Select a book to issue to a student.
- **Issue Book**: Issue a selected book to a student.
- **View Logs**: View transaction logs of issued and returned books.
- **Upload CSV**: Upload a CSV file to update book or student records.
- **Download CSV**: Download a CSV file containing book records.
- **Return Book**: Return a book that was previously issued to a student.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd library_management_system
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser account:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000/` in your web browser.

## Usage

1. Log in to the system using your credentials.
2. Navigate through the available features:
    - Manage student records.
    - Search for books and issue them to students.
    - View transaction logs.
    - Upload and download CSV files for bulk operations.
    - Return books that were issued to students.

    

    


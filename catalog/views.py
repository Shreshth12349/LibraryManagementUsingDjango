from django.shortcuts import render, redirect
from django.utils import timezone
from utils.database_management import process_csv, get_book_by_id, get_student_by_registration_no
from .models import Student, Book, Log
from django.contrib.auth.decorators import login_required
from utils.database_management import search_books as search_books_db
from utils.database_management import get_book_by_id
from .forms import BookForm
from django.contrib import messages
from django.http import HttpResponse
import csv
import tempfile
from .models import Log
# Create your views here.


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def view_students(request):
    students = Student.objects.all()
    context = {
        'students': students,
        'user_string': str(request.user),
    }
    return render(request, 'students.html', context)


@login_required
def search_students(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text', '')
        # Search for students with similar information
        students = search_books_db(search_text)
        return render(request, 'students.html', {'students': students, 'search_students': True})
    else:
        # If request method is not POST, render an empty student list
        students = Student.objects.all()
        return render(request, 'students.html', {'students': students, 'search_students': True})


@login_required
def search_books(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text', '')
        books = Book.objects.filter(
            title__icontains=search_text
        ) | Book.objects.filter(
            author__icontains=search_text
        ) | Book.objects.filter(
            book_id__icontains=search_text
        ) | Book.objects.filter(
            description__icontains=search_text
        ) | Book.objects.filter(
            availability__icontains=search_text
        ) | Book.objects.filter(
            issuedBy__icontains=search_text
        )
        return render(request, 'books.html', {'books': books, 'search_students': False})
    else:
        books = Book.objects.all()
        return render(request, 'books.html', {'books': books, 'search_students': False})


@login_required
def select_book(request):
    if request.method == 'POST':
        selected_student_registration_no = request.POST.get('selected_student')
        if selected_student_registration_no:
            selected_student = get_student_by_registration_no(selected_student_registration_no)
            # Store selected student in session
            request.session['selected_student'] = {
                'first_name': selected_student.first_name,
                'last_name': selected_student.last_name,
                'registration_no': selected_student.registration_no,
                'department': selected_student.department,
                'phone_no': selected_student.phone_no
            }
            # return redirect('home')
        else:
            messages.error(request, 'Selected student not found')
    return render(request, 'select-book.html')


@login_required
def issue_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(book_id=book_id)
            if book.availability:
                # Retrieve selected student from session
                selected_student_data = request.session.get('selected_student')
                if selected_student_data:
                    # Create or get the student object
                    selected_student, created = Student.objects.get_or_create(
                        registration_no=selected_student_data['registration_no'],
                        defaults={
                            'first_name': selected_student_data['first_name'],
                            'last_name': selected_student_data['last_name'],
                            'department': selected_student_data['department'],
                            'phone_no': selected_student_data['phone_no'],
                        }
                    )
                    # Book is available, set it as issued
                    book.availability = False
                    book.issuedBy = selected_student.registration_no
                    book.save()

                    # Add book issuance to the log
                    log_entry = Log.objects.create(
                        book_id=book.book_id,
                        issued_by=selected_student.registration_no,
                        issue_date_time=timezone.now(),
                        due_date=timezone.now() + timezone.timedelta(days=14)  # Assuming due date is 14 days from now
                    )

                    # Clear selected student from session
                    del request.session['selected_student']

                    return render(request, 'book_issued.html', {'book': book, 'log_entry': log_entry})
                else:
                    messages.error(request, 'Selected student not found')
            else:
                # Book is not available, render another page
                return render(request, 'book_not_available.html', {'book': book})
        except Book.DoesNotExist:
            # Book with the given ID does not exist
            messages.error(request, 'Book with the given ID does not exist')
    return redirect('home')


def view_logs(request):
    logs = Log.objects.all()
    return render(request, 'logs.html', {'logs': logs})


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in csv_file.chunks():
                temp_file.write(chunk)

        # Process the temporary CSV file
        process_csv(temp_file.name)

        # Delete the temporary file
        temp_file.close()

        return render(request, 'upload-success-page.html')
    else:
        return HttpResponse("No CSV file uploaded")


def get_csv(request):
    books = Book.objects.all()
    csv_content = "Book ID,Title,Author,Description,Availability,Issued By\n"
    for book in books:
        # Convert boolean values to strings
        availability = 'True' if book.availability else 'False'
        issued_by = book.issuedBy if book.issuedBy else ''  # Empty string if issuedBy is None
        csv_content += f"{book.book_id},{book.title},{book.author},{book.description},{availability},{issued_by}\n"
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    return response


def return_book(request):
    if request.method == 'POST':
        returned_book_id = request.POST.get('book_id')
        returned_book = Book.objects.get(pk=returned_book_id)
        returned_book.availability = True
        returned_book.issuedBy = None
        returned_book.save()
        log = Log.objects.filter(book_id=returned_book_id, return_status=False).first()
        log.return_status = True
        log.return_date_time = timezone.now()
        log.save()
        return render(request,  'return-success-page.html')






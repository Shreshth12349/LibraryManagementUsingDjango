from catalog.models import Student, Book
import csv

def search_books(search_text):
    students = Student.objects.filter(
        first_name__icontains=search_text
    ) | Student.objects.filter(
        last_name__icontains=search_text
    ) | Student.objects.filter(
        registration_no__icontains=search_text
    ) | Student.objects.filter(
        phone_no__icontains=search_text
    ) | Student.objects.filter(
        department__icontains=search_text
    )
    return students


def get_book_by_id(book_id):
    try:
        book = Book.objects.get(id=book_id)
        return book
    except Book.DoesNotExist:
        return None


def get_student_by_registration_no(reg_no):
    try:
        student = Student.objects.get(registration_no=reg_no)
        return student
    except Student.DoesNotExist:
        return None


def process_csv(csv_file):
    # Open the CSV file in read mode
    with open(csv_file, 'r', newline='') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Ensure the row has the expected number of fields
            if len(row) != 6:
                print("Skipping line due to incorrect format:", row)
                continue

            # Extract data from the CSV row
            book_id, title, author, description, availability_str, issued_by = row

            # Convert availability string to boolean
            availability = availability_str.lower() == 'true'

            # Check if a book with the same book_id already exists
            if not Book.objects.filter(book_id=book_id).exists():
                book = Book.objects.create(
                    book_id=book_id,
                    title=title,
                    author=author,
                    description=description,
                    availability=availability,
                    issuedBy=issued_by
                )
                book.save()
                print("Book added")
            else:
                print("Book with ID", book_id, "already exists. Skipping.")
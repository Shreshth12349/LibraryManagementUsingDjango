# forms.py

from django import forms
from .models import Book


from django import forms
from .models import Book


class BookForm(forms.Form):
    book_id = forms.IntegerField(label='Book ID')

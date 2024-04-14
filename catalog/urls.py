from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('students/', views.search_students, name='search_students'),
    path('books/', views.search_books, name='search_books'),
    path('select_book/', views.select_book, name='select_book'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('logs/', views.view_logs, name='view_logs'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('get_csv/', views.get_csv, name='get_csv'),
    path('return_book/', views.return_book, name='return_book'),
]




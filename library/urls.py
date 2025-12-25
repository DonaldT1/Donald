from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('books/', views.books, name='books'),
    path('students/', views.students, name='students'),
    path('faculties/', views.faculties, name='faculties'),
    path('book-issue/', views.book_issue, name='book_issue'),
    path('book-return/', views.book_return, name='book_return'),
    path('book-search/', views.book_search, name='book_search'),
    path('logout/', views.logout_user, name='logout'),
    path('add-book/', views.add_book, name='add_book'),
    path('borrow-book/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return-book/<int:book_id>/', views.return_book, name='return_book'),
    path('my-books/', views.my_books, name='my_books'),
]

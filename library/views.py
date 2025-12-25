from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Borrow
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import UserRegistrationForm

def home(request):
    books = Book.objects.all()
    return render(request, 'library/home.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        Borrow.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
    return redirect('home')

@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrow = Borrow.objects.filter(user=request.user, book=book, returned=False).first()
    if borrow:
        borrow.returned = True
        borrow.save()
        book.available = True
        book.save()
    return redirect('home')

@login_required
def my_books(request):
    borrows = Borrow.objects.filter(user=request.user, returned=False)
    return render(request, 'library/my_books.html', {'borrows': borrows})

# @login_required
# def registration(request):
#     return render(request, 'library/registration.html')

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional: log in user after registration
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'library/registration.html', {'form': form})

@login_required
def books(request):
    all_books = Book.objects.all()
    return render(request, 'library/books.html', {'books': all_books})


def students(request):
    students = User.objects.all()
    return render(request, 'library/students.html', {'students': students})

@login_required
def faculties(request):
    return render(request, 'library/faculties.html')

@login_required
def faculties(request):
    faculties = User.objects.filter(is_staff=True)
    return render(request, 'library/faculties.html', {'faculties': faculties})

@login_required
def book_return(request):
    borrowed_books = Borrow.objects.filter(user=request.user, returned=False)

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        borrow = Borrow.objects.filter(user=request.user, book=book, returned=False).first()

        if borrow:
            borrow.returned = True
            borrow.save()
            book.available = True
            book.save()
            messages.success(request, f'Book "{book.title}" returned successfully!')
        return redirect('book_return')

    return render(request, 'library/book_return.html', {'borrowed_books': borrowed_books})


@login_required
def book_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'library/book_search.html', {
        'results': results,
        'query': query
    })

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def book_issue(request):
    books = Book.objects.all()
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        if book.available:
            Borrow.objects.create(user=request.user, book=book)
            book.available = False
            book.save()
            messages.success(request, f'Book "{book.title}" issued successfully!')
        return redirect('book_issue')

    return render(request, 'library/book_issue.html', {'books': books})



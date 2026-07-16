from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Comment
from .forms import BookForm
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def index(request):
    latest_book_list = Book.objects.order_by('-finished')[:5]
    context = {'latest_book_list': latest_book_list}
    return render(request, 'readingjournal/index.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {
        "form": form
    })

@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect("readingjournal:index")
    else:
        form = BookForm()

    return render(request, "readingjournal/add_book.html", {
        "form": form
    })

#Flaw 4: A05 Security Misconfiguration
def detail(request, book_id):
    #try:   #Flaw 4 fix
    book = Book.objects.get(pk=book_id)
    #except Book.DoesNotExist:  #Flaw 4 fix
    #    return HttpResponse("Book does not exist", status=404)
    return render(request, 'readingjournal/detail.html', {'book': book})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id, user=request.user)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("readingjournal:detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request,"readingjournal/edit_book.html",
    {"form": form, "book": book})

#Flaw 1: A01 Broken Access Control
#@login_required #Flaw 1 fix
def delete_book(request, book_id):
    #book = get_object_or_404(Book, pk=book_id, user=request.user) #Flaw 1 fix
    book = get_object_or_404(Book, pk=book_id) #Flaw 1
    if request.method == "POST":
        book.delete()
        return redirect("readingjournal:my_books")
    
    return render(request, "readingjournal/delete_book.html", {"book": book})


def all_books(request):
    books = Book.objects.order_by("-finished")

    return render(request, "readingjournal/all_books.html", {
        "books": books
    })

@login_required
def comment(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        text = request.POST["comment"]
#Flaw 2: A03 Injection
        #Comment.objects.create(    #Flaw 2 fix
        #    book=book,
        #    user=request.user,
        #    text=text
        #)

        #Flaw 3: A04 Insecure Design
        #if not text.strip():   #Flaw 3 fix
        #    return HttpResponse("Comment cannot be empty.", status=400)
        #if len(text) > 1000:   #Flaw 3 fix
        #    return HttpResponse("Comment is too long.", status=400)
        
        with connection.cursor() as cursor: #Flaw 2
            cursor.execute(f""" INSERT INTO readingjournal_comment (book_id, user_id, text)
                           VALUES ({book.id}, {request.user.id}, '{text}')""")

    return redirect("readingjournal:detail", book_id=book.id)

@login_required
def my_books(request):
    books = Book.objects.filter(user=request.user).order_by("-finished")

    return render(request, "readingjournal/my_books.html", {
        "books": books
    })
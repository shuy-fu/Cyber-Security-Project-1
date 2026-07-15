from django.urls import path
from . import views

app_name = 'readingjournal'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('<int:book_id>/comment/', views.comment, name='comment'),
    path("add/", views.add_book, name="add_book"),
    path("mybooks/", views.my_books, name="my_books"),
    path("books/", views.all_books, name="all_books"),
    path("<int:book_id>/edit/", views.edit_book, name="edit_book"),
    path("<int:book_id>/delete/", views.delete_book, name="delete_book"),
    path("register/", views.register, name="register")
]
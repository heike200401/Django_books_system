from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    path('readers/', views.reader_list, name='reader_list'),
    path('readers/add/', views.reader_add, name='reader_add'),
    path('readers/<int:pk>/', views.reader_detail, name='reader_detail'),
    path('readers/<int:pk>/edit/', views.reader_edit, name='reader_edit'),
    path('readers/<int:pk>/delete/', views.reader_delete, name='reader_delete'),
    
    path('borrows/', views.borrow_list, name='borrow_list'),
    path('borrows/add/', views.borrow_add, name='borrow_add'),
    path('borrows/<int:pk>/', views.borrow_detail, name='borrow_detail'),
    path('borrows/<int:pk>/return/', views.borrow_return, name='borrow_return'),
]

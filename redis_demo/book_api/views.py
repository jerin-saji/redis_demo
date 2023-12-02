from django.shortcuts import render

import time 

from django.core.cache import cache
from django.http import JsonResponse
from .models import Book

def book_list(request):
    cache_key = 'book_list'
    books = cache.get(cache_key)

    if books is None:

        start_time = time.time()  # Record the start time
        # Data is not in cache, fetch it from the database
        books = list(Book.objects.values())
        cache.set(cache_key, books, 3600)  # Cache for 1 hour
        end_time = time.time()  # Record the end time
        database_time = end_time - start_time  # Calculate time taken to fetch from the database


        # Print a message to the terminal
        print("Data fetched from the database for book_list view.")
        print(f"Data fetched from the database for book_list view. Time taken: {database_time:.5f} seconds")
    else:
        start_time = time.time()  # Record the start time
        # Data is retrieved from cache
        print("Data fetched from the cache by Redis for book_list view.")
        end_time = time.time()  # Record the end time
        cache_time = end_time - start_time  # Calculate time taken to fetch from Redis cache

        print(f"Time taken to fetch from Redis cache for book_list view: {cache_time:.5f} seconds")


    return JsonResponse({'books': books})

def book_detail(request, book_id):
    cache_key = f'book_{book_id}'
    book = cache.get(cache_key)

    if book is None:
        try:
            start_time = time.time()  # Record the start time
            book = Book.objects.values().get(id=book_id)
            end_time = time.time()  # Record the end time
            database_time = end_time - start_time  # Calculate time taken to fetch from the database

        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

        cache.set(cache_key, book, 3600)  # Cache for 1 hour

        # Print a message to the terminal
        print(f"Data fetched from the database for book_detail view (book_id={book_id}).")
        print(f"Data fetched from the database for book_list view. Time taken: {database_time:.5f} seconds")

    else:
        start_time = time.time()  # Record the start time
        # Data is retrieved from cache
        print(f"Data fetched from the cache by Redis for book_detail view (book_id={book_id}).")
        end_time = time.time()  # Record the end time
        cache_time = end_time - start_time  # Calculate time taken to fetch from Redis cache

        print(f"Time taken to fetch from Redis cache for book_list view: {cache_time:.5f} seconds")


    return JsonResponse({'book': book})

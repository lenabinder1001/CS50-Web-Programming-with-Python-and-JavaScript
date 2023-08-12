import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Genre, List, Book, Goal

def index(request):
    return render(request, 'bookshelf/index.html' , {'lists': List.objects.all()})

def list(request, list_id):
    list = List.objects.get(pk=list_id)
    books = Book.objects.filter(list=list_id)

    # Pagination
    paginator = Paginator(books, 8)
    page_number = request.GET.get("page")
    page_books = paginator.get_page(page_number)

    return render(request, 'bookshelf/list.html', {'list': list, 'page_books': page_books})

def book(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'bookshelf/book.html', {'book': book})

def create(request):
    data = ""
    response = ""
    lists = List.objects.all()
    if request.method == "POST":
        if "create" in request.POST:
            title = request.POST["title"]
            content = request.POST["description"]
            author = request.POST["author"]
            pages = request.POST["pages"]
            image = request.POST["image"]
            if request.POST["rating"]:
                rating = request.POST["rating"]
            if request.POST["genre"]:
                genre = Genre.objects.get(pk=request.POST["genre"])
            if request.POST["list"]:
                list = List.objects.get(pk=request.POST["list"])
            book = Book.objects.create(title=title,
                                    content=content,
                                    author=author,
                                    pages=pages,
                                    image=image,
                                    rating=rating,
                                    genre=genre,
                                    list=list)
            book.save()
            return render(request, "bookshelf/index.html", {'lists': lists})
        if "isbnsearch" in request.POST:
            isbn = request.POST["isbn"]
            if isbn:
                response = requests.get(f'https://openlibrary.org/isbn/{isbn}.json')
                response = response.json()
                data = {}
                if 'title' in response:
                    data["title"] = response['title']
                if 'description' in response:
                    data["description"] = response['description']
                if 'number_of_pages' in response:
                    data["pages"] = int(response['number_of_pages'])
                if 'authors' in response:
                    author = response['authors'][0]['key']
                    author = requests.get(f'https://openlibrary.org{author}.json')
                    author = author.json()
                    if 'personal_name' in author:
                        data["author"] = author['personal_name']
                return render(request, 'bookshelf/create.html', {'genres': Genre.objects.all(), 'lists': List.objects.all(), "data": data})
    return render(request, 'bookshelf/create.html', {'genres': Genre.objects.all(), 'lists': List.objects.all()})
    
def edit(request, book_id):
    if request.method == "PUT":
        book = Book.objects.get(pk=book_id)
        data = json.loads(request.body)
        if data.get("title") is not None:
            book.title = data["title"]
        if data.get("author") is not None:
            book.author = data["author"]
        if data.get("pages") is not None:
            book.pages = int(data["pages"])
        if data.get("content") is not None:
            book.content = data["content"]
        if data.get("rating") is not None:
            book.rating = int(data["rating"])
        book.save()
        return JsonResponse({"message": "Change successful!"})
    
def delete(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.delete()

    return render(request, "bookshelf/index.html", {'lists': List.objects.all()})

def read_unread(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == "POST":
        if book.read == False:
            book.read = True
            book.save()
        else:
            book.read = False
            book.save()
        return render(request, "bookshelf/book.html", {'book': book})
    
def genres(request):
    return render(request, "bookshelf/genres.html", {'genres': Genre.objects.all()})

def genre(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    books = Book.objects.filter(genre=genre)

    # Pagination
    paginator = Paginator(books, 8)
    page_number = request.GET.get("page")
    page_books = paginator.get_page(page_number)

    return render(request, "bookshelf/genre.html", {'genre': genre, 'page_books': page_books})

def bookshelf_wishlist(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.list.name == 'Wishlist':
        book.list = List.objects.get(name='Bookshelf')
        book.save()
        list = List.objects.get(pk=book.list.id)
        books = Book.objects.filter(list=list.id)

        return render(request, 'bookshelf/index.html', {'lists': List.objects.all()})
    else:
        book.list = List.objects.get(name='Wishlist')
        book.save()
        list = List.objects.get(pk=book.list.id)
        list = List.objects.get(pk=book.list.id)
        books = Book.objects.filter(list=list.id)

        return render(request, 'bookshelf/index.html', {'lists': List.objects.all()})
    
def profile(request):
    books = Book.objects.filter(read=True)
    books_read = len(books)
    pages = 0
    for book in books:
        pages += book.pages

    # Get reading goals
    goal = Goal.objects.all()

    # Percent
    books_percent = books_read / goal[0].books * 100
    pages_percent = pages / goal[0].pages * 100

    # Sum books read by cagetory
    action = len(Book.objects.filter(genre=Genre.objects.get(name='Action'), read=True))
    adventure = len(Book.objects.filter(genre=Genre.objects.get(name='Adventure'), read=True))
    classics = len(Book.objects.filter(genre=Genre.objects.get(name='Classics'), read=True))
    mystery = len(Book.objects.filter(genre=Genre.objects.get(name='Mystery'), read=True))
    fantasy = len(Book.objects.filter(genre=Genre.objects.get(name='Fantasy'), read=True))
    historical_fiction = len(Book.objects.filter(genre=Genre.objects.get(name='Historical Fiction')))
    horror = len(Book.objects.filter(genre=Genre.objects.get(name='Horror'), read=True))
    romance = len(Book.objects.filter(genre=Genre.objects.get(name='Romance'), read=True))
    scifi = len(Book.objects.filter(genre=Genre.objects.get(name='Sci-Fi'), read=True))
    thriller = len(Book.objects.filter(genre=Genre.objects.get(name='Thriller'), read=True))
    womens_fiction = len(Book.objects.filter(genre=Genre.objects.get(name='Womens Fiction'), read=True))
    biography = len(Book.objects.filter(genre=Genre.objects.get(name='Biography'), read=True))

    genres = [{"Genre": "Action", 'book_count': action}, {"Genre": "Adventure", 'book_count': adventure}, {"Genre": "Classics", 'book_count': classics}, {"Genre": "Mystery", 'book_count': mystery}, {"Genre": "Fantasy", 'book_count': fantasy}, {"Genre": "Hostorical Fiction", 'book_count': historical_fiction}, {"Genre": "Horror", 'book_count': horror}, {"Genre": "Romance", 'book_count': romance}, {"Genre": "Sci-Fi", 'book_count': scifi}, {"Genre": "Thriller", 'book_count': thriller}, {"Genre": "Womens Fiction", 'book_count': womens_fiction}, {"Genre": "Biography", 'book_count': biography}]

    return render(request, 'bookshelf/profile.html', {'books_read': books_read, 'pages': pages, 'genres': genres, 'goal': goal[0], 'books_percent': books_percent, 'pages_percent': pages_percent})

def search(request):
    if request.POST:    
        if "search_author" in request.POST and request.POST["search_author"] != "":
            author_name = request.POST["search_author"]  
            books = Book.objects.filter(author__contains=author_name)
            return render(request,"bookshelf/search.html", {"books": books})
        elif "search_title" in request.POST:
            title_name = request.POST["search_title"]  
            books = Book.objects.filter(title__contains=title_name)
            return render(request,"bookshelf/search.html", {"books": books})
        else:
            return render(request, "bookshelf/search.html")
    else:
        return render(request, "bookshelf/search.html")
    
def goals(request):
    if request.method == "PUT":
        goal = Goal.objects.get()
        data = json.loads(request.body)
        if data.get("books") is not None:
            goal.books = data["books"]
        if data.get("pages") is not None:
            goal.pages = data["pages"]
        goal.save()
        return JsonResponse({"message": "Change successful!"})
    

    

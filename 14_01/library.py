from typing import Dict
from collections import Counter
import json


class Book:
    def __init__(self, book_name: str, isbn: int, author: str, genre: str, year: str) -> None:
        # ISBN проверяем сразу при создании книги,
        # чтобы в системе не появлялись заведомо некорректные объекты
        if not isinstance(isbn, int) or len(str(isbn)) not in (10, 13):
            raise ValueError("Invalid ISBN")

        self.book_name = book_name
        self.isbn = isbn
        self.author = author
        self.genre = genre
        self.year = year

        # по умолчанию книга доступна
        self.is_available = True

        # храним имя читателя, чтобы понимать, кому выдана книга
        self.reader_name: str | None = None

    def issue_book(self, reader_name: str) -> None:
        # книга сама отвечает за своё состояние
        if not self.is_available:
            raise ValueError("Book already issued")

        self.is_available = False
        self.reader_name = reader_name

    def return_book(self) -> None:
        # нельзя вернуть книгу, которая и так в библиотеке
        if self.is_available:
            raise ValueError("Book is not issued")

        self.is_available = True
        self.reader_name = None

    def __str__(self) -> str:
        # читаемый и удобный вывод
        status = "available" if self.is_available else f"issued to {self.reader_name}"
        return (
            f"Book name: {self.book_name}\n"
            f"ISBN: {self.isbn}\n"
            f"Author: {self.author}\n"
            f"Genre: {self.genre}\n"
            f"Year: {self.year}\n"
            f"Status: {status}"
        )


class Reader:
    _id = 0

    def __init__(self, name: str) -> None:
        # генерирую простой автоинкрементный id
        Reader._id += 1
        self._id = Reader._id

        self.name = name

        # Храню ISBN книг, которые находятся у читателя
        self.borrowed_books: list[int] = []


class Library:
    def __init__(self):
        # Книги храним по ISBN для быстрого доступа
        self.books: Dict[int, Book] = {}

        # Читатели хранятся по id
        self.readers: Dict[int, Reader] = {}

    def add_book(self, book: Book) -> None:
        self.books[book.isbn] = book

    def delete_book(self, isbn: int):
        # pop с дефолтом позволяет не ловить исключение выше
        return self.books.pop(isbn, "Not Found")

    def add_reader(self, reader: Reader) -> None:
        self.readers[reader._id] = reader

    def delete_reader(self, _id: int):
        return self.readers.pop(_id, "Not Found")

    def issue_book(self, reader_id: int, isbn: int):
        # библиотека отвечает за связи между объектами
        book = self.books.get(isbn)
        reader = self.readers.get(reader_id)

        if not book:
            raise ValueError("Book Not Found")
        if not reader:
            raise ValueError("Reader Not Found")

        # делегирую изменение состояния самой книге
        book.issue_book(reader.name)

        # и синхронизирую состояние читателя
        reader.borrowed_books.append(isbn)

    def return_book(self, reader_id: int, isbn: int):
        book = self.books.get(isbn)
        reader = self.readers.get(reader_id)

        if not book or not reader:
            raise ValueError("Book or Reader Not Found")

        if isbn not in reader.borrowed_books:
            raise ValueError("Reader does not have this book")

        book.return_book()
        reader.borrowed_books.remove(isbn)

    def get_statistics(self) -> dict:
        # если библиотека пустая, то вернется пустая статистика
        if not self.books:
            return {}

        # считаю распределение по жанрам и годам
        genres = Counter(book.genre for book in self.books.values())
        years = Counter(book.year for book in self.books.values())

        # возвращаю наиболее популярные значения
        return {
            "most_popular_genre": genres.most_common(1)[0][0],
            "most_popular_year": years.most_common(1)[0][0]
        }

    def save_to_json(self, filename: str) -> None:
        # сохраняю всю библиотеку одним файлом
        data = {
            "books": [
                {
                    "book_name": b.book_name,
                    "isbn": b.isbn,
                    "author": b.author,
                    "genre": b.genre,
                    "year": b.year,
                    "is_available": b.is_available,
                    "reader_name": b.reader_name
                }
                for b in self.books.values()
            ],
            "readers": [
                {
                    "id": r._id,
                    "name": r.name,
                    "borrowed_books": r.borrowed_books
                }
                for r in self.readers.values()
            ]
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_from_json(filename: str) -> "Library":
        # загружаю библиотеку целиком, восстанавливая связи
        library = Library()

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data["books"]:
            book = Book(
                item["book_name"],
                item["isbn"],
                item["author"],
                item["genre"],
                item["year"]
            )
            book.is_available = item["is_available"]
            book.reader_name = item["reader_name"]
            library.add_book(book)

        for item in data["readers"]:
            reader = Reader(item["name"])

            # восстанавливаю id, чтобы не ломать связи
            reader._id = item["id"]
            reader.borrowed_books = item["borrowed_books"]

            library.readers[reader._id] = reader
            Reader._id = max(Reader._id, reader._id)

        return library

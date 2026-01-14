import unittest
import os

from library import Book, Reader, Library


class TestBook(unittest.TestCase):

    def test_create_book_valid_isbn(self):
        # проверяю, что корректная книга создаётся без ошибок
        book = Book("1984", 1234567890, "Orwell", "Dystopia", "1949")
        self.assertTrue(book.is_available)

    def test_create_book_invalid_isbn(self):
        # некорректный ISBN должен сразу ломаться,
        # а не создавать битый объект
        with self.assertRaises(ValueError):
            Book("Wrong ISBN", 123, "Author", "Genre", "2000")

    def test_issue_book(self):
        # проверяю изменение состояния книги при выдаче
        book = Book("Dune", 1234567890123, "Herbert", "Sci-Fi", "1965")
        book.issue_book("Alice")

        self.assertFalse(book.is_available)
        self.assertEqual(book.reader_name, "Alice")

    def test_issue_already_issued_book(self):
        # повторная выдача одной и той же книги запрещена
        book = Book("Dune", 1234567890123, "Herbert", "Sci-Fi", "1965")
        book.issue_book("Alice")

        with self.assertRaises(ValueError):
            book.issue_book("Bob")

    def test_return_book(self):
        # возврат должен полностью сбрасывать состояние
        book = Book("Dune", 1234567890123, "Herbert", "Sci-Fi", "1965")
        book.issue_book("Alice")
        book.return_book()

        self.assertTrue(book.is_available)
        self.assertIsNone(book.reader_name)

    def test_return_not_issued_book(self):
        # нельзя вернуть книгу, которая не выдавалась
        book = Book("Dune", 1234567890123, "Herbert", "Sci-Fi", "1965")

        with self.assertRaises(ValueError):
            book.return_book()


class TestLibrary(unittest.TestCase):

    def set_up(self):
        # set up выполняется перед каждым тестом
        # и гарантирует чистое состояние
        self.library = Library()
        self.book = Book("1984", 1234567890, "Orwell", "Dystopia", "1949")
        self.reader = Reader("Alice")

        self.library.add_book(self.book)
        self.library.add_reader(self.reader)

    def test_issue_book(self):
        # проверяю связку книга и читатель
        self.library.issue_book(self.reader._id, self.book.isbn)

        self.assertFalse(self.book.is_available)
        self.assertIn(self.book.isbn, self.reader.borrowed_books)

    def test_return_book(self):
        self.library.issue_book(self.reader._id, self.book.isbn)
        self.library.return_book(self.reader._id, self.book.isbn)

        self.assertTrue(self.book.is_available)
        self.assertNotIn(self.book.isbn, self.reader.borrowed_books)

    def test_issue_nonexistent_book(self):
        # выдача несуществующей книги
        with self.assertRaises(ValueError):
            self.library.issue_book(self.reader._id, 9999999999)

    def test_statistics(self):
        # проверяю что статистика считает корректно
        stats = self.library.get_statistics()

        self.assertEqual(stats["most_popular_genre"], "Dystopia")
        self.assertEqual(stats["most_popular_year"], "1949")

    def test_save_and_load_json(self):
        # проверяю что сохранение и загрузка не теряют данные
        filename = "test_library.json"

        self.library.save_to_json(filename)
        loaded_library = Library.load_from_json(filename)

        self.assertEqual(len(loaded_library.books), 1)
        self.assertEqual(len(loaded_library.readers), 1)

        os.remove(filename)


if __name__ == "__main__":
    unittest.main()

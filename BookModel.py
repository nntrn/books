import json
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @classmethod
    def add_book(cls, _isbn, _name, _price):
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()

    @classmethod
    def get_all_books(cls):
        return [book.json() for book in Book.query.all()]

    @classmethod
    def get_book_by_isbn(cls, _isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    @classmethod
    def delete_book(cls, _isbn):
        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(is_successful)

    @classmethod
    def update_price(cls, _isbn, _price):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.price = _price
        db.session.commit()

    @classmethod
    def update_name(cls, _isbn, _name):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.name = _name
        db.session.commit()

    @classmethod
    def replace_book(cls, _isbn, _name, _price):
        book_to_replace = Book.query.filter_by(isbn=_isbn).first()
        book_to_replace.price = _price
        book_to_replace.name = _name
        db.session.commit()

    def json(self):
        return {'name': self.name, 'price': self.price, 'isbn': self.isbn}

    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)


if __name__ == '__main__':
    if not os.path.exists('database.db'):
        print('creating database.db')
        db.create_all()

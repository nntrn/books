import json
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    @classmethod
    def add_author(cls, _first_name, _last_name):
        new_author = Author(first_name=_first_name, last_name=_last_name)
        db.session.add(new_author)
        db.session.commit()

    @classmethod
    def get_all_authors(cls):
        return [author.json() for author in Author.query.all()]

    @classmethod
    def get_authors_by_first_name(cls, _first_name):
        return Author.json(Author.query.filter_by(first_name=_first_name))

    @classmethod
    def get_authors_by_last_name(cls, _first_name):
        return Author.json(Author.query.filter_by(first_name=_first_name))

    @classmethod
    def get_author_by_full_name(cls, _first_name, _last_name):
        return Author.json(Author.query.filter_by(first_name=_first_name, last_name=_last_name).first())

    @classmethod
    def delete_author_by_full_name(cls, _first_name, _last_name):
        is_successful = Author.query.filter_by(first_name=_first_name, last_name=_last_name).delete()
        db.session.commit()
        return bool(is_successful)

    def json(self):
        return {'author_id': self.author_id, 'first_name': self.first_name, 'last_name': self.last_name}

    def __repr__(self):
        author_object = {
            'author_id': self.author_id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        return json.dumps(author_object)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        print('creating database.db')
        db.create_all()

import sqlite3

from flask import Flask
from flask import jsonify, request

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165,
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193,
    }
]


def validate_book(book):
    required = ('name', 'price', 'isbn')
    return all([key in book for key in required])


# GET /books
@app.route('/books', methods=['GET'])
def hello_world():
    return jsonify({'books': books})


# GET /books/<isbn>
@app.route('/books/<int:isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    for book in books:
        if book['isbn'] == isbn:
            return jsonify(book)


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validate_book(request_data):
        books.insert(0, request_data)
        return "True"
    else:
        return "False"


if __name__ == '__main__':
    app.run(port=5000)

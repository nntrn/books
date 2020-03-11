import sqlite3

import json

from flask import Flask
from flask import jsonify, request, Response

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
@app.route('/books/<int:isbn>', methods=['GET'])
def get_books(isbn=None):
    if isbn is None:
        return jsonify({'books': books})
    else:
        for book in books:
            if book['isbn'] == isbn:
                return jsonify(book)


# PUT /books
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if validate_book(request_data):
        updated_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        for i, book in enumerate(books):
            if book['isbn'] == isbn:
                books[i] = updated_book
                response = Response("", 204, mimetype='application/json')
                response.headers['Location'] = '/books/' + str(updated_book['isbn'])
                return response
    else:
        return Response('Invalid book object. Must include "name", "price", and "isbn"', status=400,
                        mimetype='application/json')


# DELETE /books
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response('', status=204)
            return response
    response = Response('ISBN not found. Unable to delete.', status=404, mimetype='application/json')
    return response


# PATCH /books
@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if 'name' in request_data:
        updated_book['name'] = request_data['name']
    if 'price' in request_data:
        updated_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = 'books' + str(isbn)
    return response


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validate_book(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.append(new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        return Response('Invalid book object. Must include "name", "price", and "isbn"', status=400,
                        mimetype='application/json')


if __name__ == '__main__':
    app.run(port=5001)

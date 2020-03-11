import json
import sqlite3

from BookModel import Book
from AuthorModel import Author
from flask import Flask, render_template, Response, jsonify, request
from settings import *


def validate_book(book):
    required = ('name', 'price', 'isbn')
    return all([key in book for key in required])

# GET /
@app.route('/')
def index():
    return render_template('index.html')


# GET /books
@app.route('/books', methods=['GET'])
@app.route('/books/<int:isbn>', methods=['GET'])
def get_books(isbn=None):
    if isbn is None:
        return jsonify({'books': Book.get_all_books()})
    else:
        jsonify(Book.get_book_by_isbn(isbn))


# PUT /books
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if validate_book(request_data):
        Book.replace_book(request_data['isbn'], request_data['name'], request_data['price'])
        response = Response("", 204, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
        return response
    else:
        return Response('Invalid book object. Must include "name", "price", and "isbn"', status=400,
                        mimetype='application/json')


# DELETE /books
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response('', status=204)
        return response
    else:
        response = Response('ISBN not found. Unable to delete.', status=404, mimetype='application/json')
        return response


# PATCH /books
@app.route('/books/<int:isbn>', methods=['PATCH'])
def patch_book(isbn):
    request_data = request.get_json()
    if 'name' in request_data:
        Book.update_name(isbn, request_data['name'])
    if 'price' in request_data:
        Book.update_price(isbn, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = 'books' + str(isbn)
    return response


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validate_book(request_data):
        Book.add_book(request_data['isbn'], request_data['name'], request_data['price'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
        return response
    else:
        return Response('Invalid book object. Must include "name", "price", and "isbn"', status=400,
                        mimetype='application/json')


# allow both GET and POST requests
@app.route('/add-book', methods=['GET', 'POST'])
def add_book_form():
    
    # this block is only entered when the form is submitted
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        name = request.form['name']
        price = request.form['price']
        
        Book.add_book(isbn, name, price)

        return '''<h1>You added a new book!</h1>
                  <div>{}, {}, ${}</div>
                  <a href="/">View</a>'''.format(isbn, name, price)

    return '''<form method="POST">
                  ISBN: <input type="number" value="12" name="isbn"><br>
                  Framework: <input type="text" value="How Things Happen..." name="name"><br>
                  Price: <input type="number" value="20.00" min="0.01" step="0.01" max="2500" name="price"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


if __name__ == '__main__':
    app.run(port=5001)

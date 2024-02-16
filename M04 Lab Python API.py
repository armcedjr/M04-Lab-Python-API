# -*- coding: utf-8 -*-
"""
Armando Cedano
M04 Lab
This code defines a Flask application with routes for creating, reading, updating, and deleting books in a SQLite database. The database connection is managed within each route function.
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY, book_name TEXT, author TEXT, publisher TEXT)''')
conn.commit()
conn.close()

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# API Routes

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    conn = get_db_connection()
    data = request.get_json()
    try:
        book_name = data['book_name']
        author = data['author']
        publisher = data['publisher']
        # Insert the new book into the database
        conn.execute('INSERT INTO books (book_name, author, publisher) VALUES (?, ?, ?)',
                     (book_name, author, publisher))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book created successfully'}), 201
    except KeyError:
        return jsonify({'error': 'Missing required parameters in request'}), 400

# Retrieve all books
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])

# Retrieve a specific book by id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is not None:
        return jsonify(dict(book))
    else:
        return jsonify({'error': 'Book not found'}), 404

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    conn = get_db_connection()
    data = request.get_json()
    try:
        book_name = data['book_name']
        author = data['author']
        publisher = data['publisher']
        # Update the book in the database
        conn.execute('UPDATE books SET book_name = ?, author = ?, publisher = ? WHERE id = ?',
                     (book_name, author, publisher, book_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book updated successfully'})
    except KeyError:
        return jsonify({'error': 'Missing required parameters in request'}), 400

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    # Delete the book from the database
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

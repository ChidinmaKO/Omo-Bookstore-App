from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

from server.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    BOOKS = [
        {
            'id': uuid.uuid4().hex,
            'title': 'On the Road',
            'author': 'Jack Kerouac',
            'read': True
        },
        {
            'id': uuid.uuid4().hex,
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J. K. Rowling',
            'read': False
        },
        {
            'id': uuid.uuid4().hex,
            'title': 'Green Eggs and Ham',
            'author': 'Dr. Seuss',
            'read': True
        }
    ]

    @app.route('/books', methods=['GET', 'POST'])
    def all_books():
        ''' Adds and gets books '''
        # TODO: Seperate POST & GET Methods
        response_object = {'status': 'success'}

        if request.method == 'POST':
            post_data = request.get_json()
            BOOKS.append({
                'id': uuid.uuid4().hex,
                'title': post_data.get('title'),
                'author': post_data.get('author'),
                'read': post_data.get('read')
            })
            response_object['message'] = 'Book added!'
        else:
            response_object['books'] = BOOKS
        return jsonify(response_object)

    @app.route('/books/<book_id>', methods=['PUT'])
    def single_book(book_id):
        response_object = {'status': 'success'}
        if request.method == 'PUT':
            post_data = request.get_json()
            remove_book(book_id)

            BOOKS.append({
                'id': uuid.uuid4().hex,
                'title': post_data.get('title'),
                'author': post_data.get('author'),
                'read': post_data.get('read')
            })
            response_object['message'] = 'Book updated!'
        else:
            response_object['books'] = BOOKS
        return jsonify(response_object)

    def remove_book(book_id):
        for book in BOOKS:
            if book['id'] == book_id:
                BOOKS.remove(book)
                return True
        return False

    return app
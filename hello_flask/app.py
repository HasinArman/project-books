# Import necessary modules from Flask and Flask-SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure Flask app to use SQLite database named 'library.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

# Create an instance of the SQLAlchemy class
db = SQLAlchemy(app)

# Define the Book model using SQLAlchemy
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

# Create the database tables based on the models
db.create_all()

# Route to display a list of books
@app.route('/books')
def list_books():
    # Query all books from the database
    all_books = Book.query.all()
    # Render the books.html template and pass the books list to it
    return render_template('books.html', books=all_books)

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_new_book():
    if request.method == 'POST':
        # Retrieve book data from the form
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        # Create a new Book object with the provided data
        new_book = Book(title=title, author=author, publication_year=publication_year)

        # Add the new book to the database session
        db.session.add(new_book)
        # Commit the changes to the database
        db.session.commit()

        # Redirect the user to the books page after adding the new book
        return redirect(url_for('list_books'))

    # Render the add_book.html template for GET requests
    return render_template('add_book.html')

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)

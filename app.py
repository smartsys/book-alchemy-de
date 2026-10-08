from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import date
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/')
def home():
    sort = request.args.get('sort')
    query = db.select(Book)

    if sort == 'title':
        query = query.order_by(Book.title)
    elif sort == 'author':
        query = query.join(Book.author).order_by(Author.name)

    books = db.session.execute(query).scalars().all()

    return render_template('home.html', books=books, sort=sort)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    message = None
    if request.method == 'POST':
        date_of_death = request.form.get('date_of_death')
        author = Author(
            name=request.form.get('name'),
            birth_date=date.fromisoformat(request.form.get('birthdate')),
            date_of_death=date.fromisoformat(date_of_death) if date_of_death else None
        )
        db.session.add(author)
        db.session.commit()
        message = f"Author {author.name} was added successfully."
    return render_template('add_author.html', message=message)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    message = None
    if request.method == 'POST':
        publication_year = request.form.get('publication_year')
        book = Book(
            isbn=request.form.get('isbn'),
            title=request.form.get('title'),
            publication_year=int(publication_year) if publication_year else None,
            author_id=int(request.form.get('author_id'))
        )
        db.session.add(book)
        db.session.commit()
        message = f"Book {book.title} was added successfully."
    authors = db.session.execute(db.select(Author).order_by(Author.name)).scalars().all()
    return render_template('add_book.html', authors=authors, message=message)


with app.app_context():
    # db.create_all()
    pass

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
import random
from pathlib import Path
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class QuoteModel(db.Model):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(32))
    text: Mapped[str] = mapped_column(String(255))
    #rating = db.Column(db.Integer(), default=1)

    def __init__(self, author, text, rating=1):
        self.author = author
        self.text  = text
        self.rating = rating

    def to_dict(self):
        new_dict = {
            'id': self.id,
            'author': self.author,
            'text': self.text,
            #'rating': self.rating
        }
        return new_dict


@app.route('/quotes')
def get_quotes():
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    quotes = []
    for quote in quotes_db:
        temp_quote = quote.to_dict()
        quotes.append(temp_quote)
    return jsonify(quotes), 200


@app.route('/quotes/<int:quote_id>')
def get_quote_id(quote_id):
    answer = db.session.get(QuoteModel, quote_id)
    if answer is not None:      
        quote = answer.to_dict()
        return jsonify(quote), 200
    return {'error': f'Quote with this id={quote_id} not found!'}, 404


@app.route('/quotes/count')
def get_quotes_count():
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()  
    number_quotes = len(quotes_db)
    data_count = {'count': number_quotes}
    return data_count


@app.route('/quotes', methods=['POST'])
def create_quote():
    new_quote = request.json     # json -> dict
    q = QuoteModel(new_quote['author'], new_quote['text'])
    db.session.add(q)
    db.session.commit()
    answer = q.id
    new_quote['id'] = answer
    return jsonify(new_quote), 201


@app.route('/quotes/<int:id>', methods=['PUT'])
def edit_quote(id):
    answer = db.session.get(QuoteModel, id)
    if answer is None:     # проверка наличия записи в БД
        return {'error': f'Quote with this id={id} not found!'}, 404
    else:
        new_data = request.json     # json -> dict
        if 'author' in new_data:
            answer.author = new_data['author']
        if 'text' in new_data:
            answer.text = new_data['text']
        db.session.commit()
        quote = answer.to_dict()
        return jsonify(quote), 200


@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    answer = db.session.get(QuoteModel, quote_id)
    if answer is None:     # проверка наличия записи в БД
        return {'error': f'Quote with this id={quote_id} not found!'}, 404
    else:
        db.session.delete(answer)
        db.session.commit()
        return jsonify({'message': f'Quote with id={quote_id} has deleted!'}), 200
       

@app.route('/quotes/filter', methods=['GET'])
def search():
    args = request.args
    author = args.get('author')
    if author is not None:
        #answer = db.session.execute(db.select(QuoteModel).order_by(QuoteModel.author)).scalars()
        answer = db.session.query(QuoteModel).filter_by(author=author).all()
        if answer:     # проверка наличия записи в БД
            quotes = []
            for quote in answer:
                temp_quote = quote.to_dict()
                quotes.append(temp_quote)
                return jsonify(quotes), 200
        else:
            return {'error': f'Quotes with such filters were not found!'}, 404


if __name__ == '__main__':
    app.run(debug=True)


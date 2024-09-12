from flask import Flask, jsonify, request
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
    'name': 'Алексей',
    'surname': 'Тихонов',
    'email': 'leopard@mail.ru'
}

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
       "rating": 1
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
       "rating": 2
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
       "rating": 3
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так.",
       "rating": 4
   },
]


def check_rating(quote):
    if quote['rating'] > 5 or quote['rating'] < 1:
        quote['rating'] = 1    


@app.route('/')
def hello_world():
    return jsonify(hello='Hello, World!'), 200


@app.route('/about')
def about():
    return jsonify(about_me), 200


@app.route('/quotes')
def get_quotes():
    return quotes


@app.route('/quotes/<int:quote_id>')
def get_quote_id(quote_id):
    for element in quotes:
        if element['id'] == quote_id:
            return element, 200
    return f'Цитаты с номером {quote_id} нету!!!', 404


@app.route('/quotes/count')
def get_quotes_count():
    count_quotes = len(quotes) 
    data_count = {'count': count_quotes}
    return data_count


@app.route('/quotes/random', methods=['GET'])
def get_quotes_random():
    size_quotes = len(quotes)
    lst = list(range(0, size_quotes))
    random_number = random.choice(lst)
    return quotes[random_number]


@app.route('/quotes', methods=['POST'])
def create_quote():
    new_quote = request.json     # json -> dict
    new_id = quotes[-1]['id'] + 1
    new_quote['id'] = new_id
    if 'rating' in new_quote:       # проверка передан ли рейтинг
        check_rating(new_quote)     # проверка рейтинга на валидность
    else:
        new_quote['rating'] = 1
    quotes.append(new_quote)
    return jsonify(new_quote), 201


@app.route('/quotes/<int:id>', methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    for element in quotes:
        if element['id'] == id:
            if 'author' in new_data:
                new_author = new_data['author']
                element['author'] = new_author
            if 'text' in new_data:
                new_text = new_data['text']
                element['text'] = new_text 
            if 'rating' in new_data:
                check_rating(new_data)         # проверка рейтинга на валидность
                new_rating = new_data['rating']
                element['rating'] = new_rating     
            return element, 200
    return {'error': f'Quote with this id={id} not found!'}, 404


@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    for quote in quotes:
        if quote['id'] == quote_id:
            quotes.remove(quote)
            return jsonify({'message': f'Quote with id={quote_id} has deleted'}), 200
    return {'error': f'Quote with this id={quote_id} not found!'}, 404    


@app.route('/quotes/filter', methods=['GET'])
def search():
    args = request.args
    author = args.get('author')
    rating = args.get('rating')
    if rating is not None:
        rating = int(rating)
    lst = []
    if (author is not None) and (rating is not None):
        for element in quotes:
            if element['author'] == author and element['rating'] == rating:
                lst.append(element)
    if (author is not None) and (rating is None):
        for element in quotes:
            if element['author'] == author:
                lst.append(element)
    if (author is None) and (rating is not None):
        for element in quotes:
            if element['rating'] == rating:
                lst.append(element)
    if len(lst) != 0:
        return lst, 200
    else:
        return {'error': f'Quotes with such filters were not found!'}, 404


if __name__ == '__main__':
    app.run(debug=True)


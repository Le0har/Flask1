from flask import Flask, jsonify, request
import random
from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "test.db"  # <- тут путь к БД

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# about_me = {
#     'name': 'Алексей',
#     'surname': 'Тихонов',
#     'email': 'leopard@mail.ru'
# }

# quotes = [
#    {
#        "id": 3,
#        "author": "Rick Cook",
#        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
#        "rating": 1
#    },
#    {
#        "id": 5,
#        "author": "Waldi Ravens",
#        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
#        "rating": 2
#    },
#    {
#        "id": 6,
#        "author": "Mosher’s Law of Software Engineering",
#        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
#        "rating": 3
#    },
#    {
#        "id": 8,
#        "author": "Yoggi Berra",
#        "text": "В теории, теория и практика неразделимы. На практике это не так.",
#        "rating": 4
#    },
# ]


def check_rating(quote):
    if quote['rating'] > 5 or quote['rating'] < 1:
        quote['rating'] = 1    


# @app.route('/')
# def hello_world():
#     return jsonify(hello='Hello, World!'), 200


# @app.route('/about')
# def about():
#     return jsonify(about_me), 200


@app.route('/quotes')
def get_quotes():
    """Функция неявно преобразовывает список словарей в JSON"""
    select_quotes = "SELECT * FROM quotes"
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall()  # get list[tuple]
    cursor.close()
    connection.close()
    # Подготовка данных для отправки в правильном формате (список словарей)
    keys = ('id', 'author', 'text')
    quotes = []
    for quote_db in quotes_db:
        quote = dict(zip(keys, quote_db))
        quotes.append(quote)
    return jsonify(quotes), 200


@app.route('/quotes/<int:quote_id>')
def get_quote_id(quote_id):
    select_quote = "SELECT * FROM quotes WHERE id = ?"
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quote, (quote_id,))
    answer = cursor.fetchone()
    cursor.close()
    connection.close()
    if answer is not None:      # !!! Верно ли так?
        keys = ('id', 'author', 'text')
        quote = dict(zip(keys, answer))
        return jsonify(quote), 200
    return {'error': f'Quote with this id={quote_id} not found!'}, 404


@app.route('/quotes/count')
def get_quotes_count():
    # count_quotes = len(quotes)
    select_quote = "SELECT COUNT(*) FROM quotes"
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quote)
    answer = cursor.fetchone()
    cursor.close()
    connection.close()  
    data_count = {'count': answer[0]}
    return data_count


# @app.route('/quotes/random', methods=['GET'])
# def get_quotes_random():
#     size_quotes = len(quotes)
#     lst = list(range(0, size_quotes))
#     random_number = random.choice(lst)
#     return quotes[random_number]


@app.route('/quotes', methods=['POST'])
def create_quote():
    new_quote = request.json     # json -> dict
    print(new_quote)
    # new_id = quotes[-1]['id'] + 1
    # new_quote['id'] = new_id
    # if 'rating' in new_quote:       # проверка передан ли рейтинг
    #     check_rating(new_quote)     # проверка рейтинга на валидность
    # else:
    #     new_quote['rating'] = 1
    select_quote = "INSERT INTO quotes (author, text) VALUES (?, ?)"
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quote, (new_quote['author'], new_quote['text']))
    answer = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    new_quote['id'] = answer
    #quotes.append(new_quote)
    return jsonify(new_quote), 201


@app.route('/quotes/<int:id>', methods=['PUT'])
def edit_quote(id):
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    check_id = "SELECT EXISTS(SELECT * FROM quotes WHERE id = ?)"   # проверка наличия записи в БД
    cursor.execute(check_id, (id,))
    answer = cursor.fetchone()
    answer = answer[0]
    if answer == 0:     # проверка наличия записи в БД
        cursor.close()
        connection.close()
        return {'error': f'Quote with this id={id} not found!'}, 404
    else:
        new_data = request.json     # json -> dict
        if 'author' in new_data:
            cursor.execute("UPDATE quotes SET author = ? WHERE id = ?", (new_data['author'], id))
        if 'text' in new_data:
            cursor.execute("UPDATE quotes SET text = ? WHERE id = ?", (new_data['text'], id))
        connection.commit()

        cursor.execute("SELECT * FROM quotes WHERE id = ?", (id,))
        answer = cursor.fetchone()
        cursor.close()
        connection.close()
        keys = ('id', 'author', 'text')
        quote = dict(zip(keys, answer))
        return jsonify(quote), 200
    
    # for element in quotes:
    #     if element['id'] == id:
    #         if 'author' in new_data:
    #             new_author = new_data['author']
    #             element['author'] = new_author
    #         if 'text' in new_data:
    #             new_text = new_data['text']
    #             element['text'] = new_text 
    #         if 'rating' in new_data:
    #             check_rating(new_data)         # проверка рейтинга на валидность
    #             new_rating = new_data['rating']
    #             element['rating'] = new_rating     
    #         return element, 200
    


@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    # for quote in quotes:
    #     if quote['id'] == quote_id:
    #         quotes.remove(quote)

    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    check_id = "SELECT EXISTS(SELECT * FROM quotes WHERE id = ?)"   # проверка наличия записи в БД
    cursor.execute(check_id, (quote_id,))
    answer = cursor.fetchone()
    answer = answer[0]
    if answer == 0:     # проверка наличия записи в БД
        cursor.close()
        connection.close()
        return {'error': f'Quote with this id={quote_id} not found!'}, 404
    else:
        cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': f'Quote with id={quote_id} has deleted!'}), 200
       


@app.route('/quotes/filter', methods=['GET'])
def search():
    args = request.args
    author = args.get('author')
    if author is not None:
        connection = sqlite3.connect("store.db")
        cursor = connection.cursor()
        check_author = "SELECT EXISTS(SELECT * FROM quotes WHERE author = ?)"   # проверка наличия записи в БД
        cursor.execute(check_author, (author,))
        answer = cursor.fetchone()
        answer = answer[0]
        if answer == 0:     # проверка наличия записи в БД
            cursor.close()
            connection.close()
            return {'error': f'Quotes with such filters were not found!'}, 404
        else:
            select_filter = "SELECT * FROM quotes WHERE author = ?"
            cursor.execute(select_filter, (author,))
            answer = cursor.fetchall()
            cursor.close()
            connection.close()
            keys = ('id', 'author', 'text')
            quotes = []
            for element in answer:
                quote = dict(zip(keys, element))
                quotes.append(quote)
            return jsonify(quotes), 200
  

    # rating = args.get('rating')
    # if rating is not None:
    #     rating = int(rating)
    # lst = []
    # if (author is not None) and (rating is not None):
    #     for element in quotes:
    #         if element['author'] == author and element['rating'] == rating:
    #             lst.append(element)
    # if (author is not None) and (rating is None):
    #     for element in quotes:
    #         if element['author'] == author:
    #             lst.append(element)
    # if (author is None) and (rating is not None):
    #     for element in quotes:
    #         if element['rating'] == rating:
    #             lst.append(element)
    # if len(lst) != 0:
    #     return lst, 200
    # else:
    #     return {'error': f'Quotes with such filters were not found!'}, 404


if __name__ == '__main__':
    app.run(debug=True)


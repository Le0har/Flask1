from flask import Flask
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
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
   },
   {
       "id": 6,
       "author": "Mosher’s Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так."
   },
]


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/about')
def about():
    return about_me


@app.route('/quotes')
def get_quotes():
    return quotes


@app.route('/quotes/<int:quote_id>')
def get_quotes_id(quote_id):
    for element in quotes:
        if element['id'] == quote_id:
            return element['text']
    return f'Цитаты с номером {quote_id} нету!!!', 404


@app.route('/quotes/count')
def get_quotes_count():
    count_quotes = len(quotes) 
    data_count = {'count': count_quotes}
    return data_count


@app.route('/quotes/random')
def get_quotes_random():
    size_quotes = len(quotes)
    lst = list(range(0, size_quotes))
    random_number = random.choice(lst)
    return quotes[random_number]['text']


if __name__ == '__main__':
    app.run(debug=True)


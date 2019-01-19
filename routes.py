from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import wikipedia

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'wittyhacks'
app.config['MONGO_URI'] = 'mongodb://Sarthak:Sarthak98@ds161134.mlab.com:61134/wittyhacks'

mongo = PyMongo(app)
# two decorators, same function


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Tiger Home Page')
     

@app.route('/home', methods=['POST'])
def my_form():
    text = request.form['searchStr']
    content = mongo.db.content
    content.insert({'topic':text, data': wikipedia.summary(text)})
    return "Added!"


# print(wikipedia.summary("google", sentences=3))

# page = wikipedia.page("indira gandhi")
# print(page.content)
# print(page.title)
# print(page.images[0])

# @app.route('/symbol.html')
# def symbol():
#     return render_template('symbol.html', the_title='Tiger As Symbol')


# @app.route('/myth.html')
# def myth():
#     return render_template('myth.html', the_title='Tiger in Myth and Legend')

if __name__ == '__main__':
    app.run(debug=True)

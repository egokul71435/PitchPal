from flask import Flask
from threading import Thread

app = Flask('')
# create a webserver object @app.route('/') # define a route with @app.route('/')

@app.route('/')
# define a view function

def home():
    return "Hello. I am alive!"


def run():
  app.run(host='0.0.0.0',port=8080)

# create a thread object

def keep_bot_alive():
  t = Thread(target=run)
  t.start()

# run the flask app
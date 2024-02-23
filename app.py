from flask import Flask

from views import view

app = Flask(__name__)
app.register_blueprint(view.elevator_blue)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

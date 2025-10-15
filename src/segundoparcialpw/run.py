from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hola, Juan!'

if __name__ == "_main_":
    app.run(debug=True)

import flask
import os

app = flask.Flask(__name__)
data = ''  # Global variable to store data

@app.route('/input/<passw>/<data>', methods=['POST', 'GET'])
def input(passw, data):
    if passw == '3645':
        with open('data.txt', 'w+') as f:
            f.write(data)
        return 'Data written successfully <3'  # Response when data is written

@app.route('/data', methods=['POST', 'GET'])
def get_data():
    with open("data.txt", "r") as f:
        return str(f.read())  # Returns the contents of data.txt

@app.route('/', methods=['POST', 'GET'])
def main():
    return str(app.url_map)  # Returns the URL map of the Flask app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))

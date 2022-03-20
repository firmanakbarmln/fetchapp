import flask
import fetchapp
from flask import request, Flask

app = flask.Flask(__name__)

@app.route('/')
@app.route('/api/fetch', methods=['POST'])
def fetch():
    fetch = fetchapp.Fetch.fetchData()
    return fetch

@app.route('/api/claim', methods=['POST'])
def claim():
    claim = fetchapp.Fetch.claim()
    return claim

@app.route('/api/aggregation', methods=['POST'])
def aggregation():
    aggregation = fetchapp.Fetch.aggregation()
    return aggregation

@app.route('/api/login', methods=['POST'])
def login():
    nik = request.form['nik']
    password = request.form['password']
    login = fetchapp.Fetch.login(nik, password)
    return login

if __name__ == '__main__':
    app.run(debug = True)
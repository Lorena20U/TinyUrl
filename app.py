from flask import Flask, request, redirect, url_for
from jinja2 import Template, Environment, FileSystemLoader
import redis

file_loader = FileSystemLoader('templates')
env = Environment(loader = file_loader)

app = Flask(__name__)

@app.route('/')
def index():
    template = env.get_template('tiny.html')
    return template.render()

@app.route('/urls')
def urlsList():
    template = env.get_template('urls.html')
    return template.render()

@app.route('/stats')
def stat():
    template = env.get_template('stats.html')
    return template.render()


@app.route('/search')
def search():
    template = env.get_template('search.html')
    return template.render()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug = True)
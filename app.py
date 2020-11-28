from flask import Flask, request, redirect, url_for
from jinja2 import Template, Environment, FileSystemLoader
import datetime
import random
import string
import redis
import os

REDIS_HOST= os.getenv("REDIS_HOST", None)
p = redis.StrictRedis(host=REDIS_HOST, port=6379, charset="UTF-8", decode_responses=True)


file_loader = FileSystemLoader('templates')
env = Environment(loader = file_loader)

app = Flask(__name__)

def token(u: str, id: str) -> str:
    #Generar 
    tok = ""
    if u == "":
        return tok
    if id == "":
        for i in range(5):
            tok += f"{random.choice(string.ascii_uppercase)}"
        return tok
    if id != "":
        tok += f"{id}"
        return tok

def creacion() -> str:
    #fecha
    t =""
    t += f"{(datetime.datetime.now())}"
    return t


def dat(ur: str, tk:str) -> dict:
    data={}
    if ur == "":
        return data
    if ur != "":
        key = tk
        data['creacion'] = creacion()
        data['token'] = key
        data['url'] = ur
        data['visitas'] = 0
        p.hset(key, None, None, data)
        return data

def listar()->dict:
    #obtener
    d = {}
    y = p.keys()
    if (y):
        for k in y:
            d[k] = p.hgetall(k)
    print (p.keys())
    return d

@app.route('/', methods=["GET", "POST"])
def index():
    url = request.form.get("link", "")
    cust = request.form.get("custom", "")
    nuevo = token(url, cust)
    tt = dat(url, nuevo)
    l=url
    template = env.get_template('tiny.html')
    return template.render(respuesta=nuevo, l=l)

@app.route('/urls')
def urlsList():
    el = request.form.get("elim", "")
    p.delete(f'{el}')
    e = listar()
    template = env.get_template('urls.html')
    return template.render(e=e)

@app.route('/stats')
def stat():
    t = listar()
    template = env.get_template('stats.html')
    return template.render(t=t)

@app.route('/search')
def search():
    b = request.form.get("busc", "")
    sea = {}
    yy = p.keys("*")
    if (yy):
        for s in yy:
            if (s == b):
                sea[s]= p.hgetall(s)
    template = env.get_template('search.html')
    return template.render(sea=sea)
    
@app.route('/<token>')
def entr(token):
    urlResponse = p.hget(token, 'url')
    print(p.hget(token, 'url'))
    v = int(p.hget(token, 'visitas'))+1
    p.hset(token, 'visitas', v)
    print (urlResponse)
    return redirect(urlResponse)




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug = True)
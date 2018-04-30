from flask import Flask, render_template, render_template_string, abort, request, g, redirect, url_for
from random import randint
import sqlite3
import requests

app = Flask(__name__)

def db_connect():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    return c


@app.before_request
def before_connect():
    print ("db connected")
    g.db = db_connect()

@app.route('/')
def home():
    authors_lst = ['jyothish', 'james', 'rody']
#    return render_template('author.html', authors_lst=authors_lst)
#    return render_template('home-page.html')
#    return render_template('jscript.html')
    return render_template('b_strap.html')


@app.route('/car')
def caro():
#    return render_template('carousel.html')
    return render_template('divide.html')

@app.route('/authors/<string:author_name>/')
def authors(author_name):
    user_info = {
    "jyothish": {"full_name": "Jyothish Kumar S", "nationality": "indian"},
    "james": {"full_name": "james Rodriguz", "nationality": "us"},
    "rody": {"full_name": "Rody Ronz", "nationality": "canada"}
    }

    if author_name not in user_info:
        abort(404)

    return render_template('authors.html', athr_name=user_info[author_name]["full_name"], athr_cntry=user_info[author_name]["nationality"])

@app.route('/info')
def user_redirect():
    return render_template('redirect.html')


@app.route('/update_info', methods=['GET', 'POST'])
def user_update():
    try:
        if request.method == 'POST':
            conn = sqlite3.connect('store.db')
            c = conn.cursor()
            name = request.form['name']
            dob = request.form['birthday']
            email = request.form['id']
            c.execute("insert into data values(?,?,?)", (name, dob, email))
            conn.commit()
            return render_template('thanks.html')

        elif request.method == 'GET':
             return render_template('update.html')

    except sqlite3.IntegrityError as e:
        return redirect(url_for('user_redirect'))


@app.route('/request_info')
def request_info():
    for key,value in request.headers:
        print (key, value)
    c_ip = requests.get('http://freegeoip.net/json').json()
    return render_template('request.html', ip=c_ip['ip'], country=c_ip['country_name'], timezone=c_ip['time_zone'])


@app.route('/users/<user_name>/')
def rand(user_name):
    quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    r_quote = randint(0, len(quotes) - 1)
    quote = quotes[r_quote]
    return render_template('users.html', **locals())


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='172.17.7.68')

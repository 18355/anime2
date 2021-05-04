from flask import Flask,g,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'anime.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def home():
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime")
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("user_test.html", results=results)

@app.route("/anime/<int:anime>")
def page(anime):
    print(anime)
    return render_template("user_test.html", results=results)

    
if __name__ == "__main__":
    app.run(debug=True)



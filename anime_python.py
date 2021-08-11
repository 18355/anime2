from flask import Flask, flash,g,render_template,request,redirect,url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] =  16 * 1024 * 1024

DATABASE = 'anime.db'
ALLOWED_EXTENTIONS = set(['png','jpg','jpeg', 'gif'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)      
    return db 

@app.route("/") #homepage
def home():
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime")
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("user_test.html", results=results)


@app.route("/") #2ndpage
def second_page():
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime")
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("onepiece.html", results=results)

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route("/anime/<int:anime>")         #linking to other pages
def page(anime):
    print(anime)
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime where id=?")
    cursor.execute(sql,(anime, ))
    results = cursor.fetchone()
    cursor = get_db().cursor()
    sql = ("SELECT * FROM picture where anime_id =?")
    cursor.execute(sql,(anime, ))
    pics = cursor.fetchall()
    return render_template("onepiece.html", item=results, pics = pics)


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        id = request.form.get("id")
        cursor = get_db()
        sql = "INSERT INTO picture (filename, anime_id) VALUES (?,?);"
        cursor.execute(sql,(filename, id))
        get_db().commit()
        return redirect(url_for("page", anime=id))
        # return render_template('onepiece.html', filename=filename)
    else:
        return redirect(url_for("home"))

@app.route('/delete', methods=["GET","POST"]) #delete an image
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["picture_id"])
        anime_id = int(request.form["anime_id"])
        sql = "DELETE FROM picture WHERE id = ?;"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect(url_for("page", anime=anime_id))

@app.route('/anime/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/'+filename), code=301)
    
if __name__ == "__main__":
    app.run(debug=True)



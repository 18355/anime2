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
    db = getattr(g, '_database', None)    #Connects to the sql 'anime.db' folder to python
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)      
    return db 

@app.route("/") #homepage
def home():
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime") #Selects all the inf from SQL and present it on html
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("user_test.html", results=results) #refresh


@app.route("/") #2ndpage, when clicked a specific anime button
def second_page():
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime") #Selects all the inf from SQL and present it on html
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("onepiece.html", results=results)

@app.route("/news") #activate the news page html
def news():
    return render_template("news.html")

@app.route("/contact") #activates the contact page (nav bar) 
def contact():
    return render_template("contact.html")

@app.route("/about") #activates the about page (nav bar) 
def about():
    return render_template("about.html")

@app.route("/help") #activates the help page (nav bar) 
def help():
    return render_template("help.html")


def allowed_file(filename):  #uploading image file, activating the file name 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS  #only allows allowed file types

@app.route("/anime/<int:anime>")       #select a specific anime, and link to the folder that stores the files of the specific anime
def page(anime):
    print(anime)
    cursor = get_db().cursor()
    sql = ("SELECT * FROM anime where id=?") #Select an anime from id
    cursor.execute(sql,(anime, ))
    results = cursor.fetchone()
    cursor = get_db().cursor()
    sql = ("SELECT * FROM picture where anime_id =?") #select the storage folder for the anime
    cursor.execute(sql,(anime, ))
    pics = cursor.fetchall()
    return render_template("onepiece.html", item=results, pics = pics)


@app.route('/upload', methods=['POST'])   #upload the selected image to the page
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        id = request.form.get("id")       #anime name
        cursor = get_db()
        sql = "INSERT INTO picture (filename, anime_id) VALUES (?,?);"   #Upload the selected file to the sql database
        cursor.execute(sql,(filename, id))
        get_db().commit()
        return redirect(url_for("page", anime=id))
        # return render_template('onepiece.html', filename=filename)
    else:
        return redirect(url_for("second_page"))

@app.route('/delete', methods=["GET","POST"]) #delete the selected image from the page
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["picture_id"])
        anime_id = int(request.form["anime_id"])
        sql = "DELETE FROM picture WHERE id = ?;"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect(url_for("page", anime=anime_id))

@app.route('/anime/<filename>')  #Get the file and present it on the page
def display_image(filename):
    return redirect(url_for('static', filename='uploads/'+filename), code=301)
    
if __name__ == "__main__":  #run the program with debug
    app.run(debug=True)



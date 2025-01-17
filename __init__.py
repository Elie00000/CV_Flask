from flask import Flask, render_template_string, render_template, jsonify, url_for
from flask import Flask, render_template, request, redirect
from flask import json
from urllib.request import urlopen
import sqlite3
import traceback
                                                                                                                                       
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("cv.html")


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    try:
        if request.method == 'POST':
            # Récupérer les données du formulaire test test
            email = request.form['email']
            message = request.form['message']

            # Insérer les données dans la base de données
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO messages (email, message) VALUES (?, ?)', (email, message))
                conn.commit()

            # Rediriger vers la page de consultation des messages après l'ajout
            return redirect(url_for('ReadBDD'))

        # Si la méthode est GET, simplement rendre le template du formulaire
        return render_template('messages.html')

    except Exception as e:
        print("Une erreur s'est produite : ", str(e))
        print(traceback.format_exc())
        return str(e), 500



@app.route("/consultation/")
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages;')
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/delete_all', methods=['GET'])
def delete_all():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
    return redirect(url_for('ReadBDD'))



if(__name__ == "__main__"):
    app.run()

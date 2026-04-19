from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__, template_folder=".")

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            course TEXT,
            teacher TEXT,
            rating TEXT,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/view')
def view_feedback():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    data = c.fetchall()
    conn.close()
    return render_template('view.html', data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---------------- FORM SUBMIT ----------------
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    fullname = request.form['fullname']
    course = request.form['course']
    teacher = request.form['teacher']
    rating = request.form['rating']
    comments = request.form['comments']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO feedback (fullname, course, teacher, rating, comments)
        VALUES (?, ?, ?, ?, ?)
    ''', (fullname, course, teacher, rating, comments))
    conn.commit()
    conn.close()

    return redirect('/view')  # go to view page after submit

if __name__ == '__main__':
    app.run(debug=True)
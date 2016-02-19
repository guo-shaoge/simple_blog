from flask import Flask, render_template, redirect, g, request, flash, \
        session, url_for
from contextlib import closing
from datetime import datetime
from backup_file import backup_diary
import sqlite3

SECRET_KEY = 's simple key'
DATABASE = 'flaskr.db'
DEBUG = True
USERNAME = '1'
PASSWORD = '1'

app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	cur = g.db.execute('select title, text, time from entries order by id desc')
	entries = [dict(title=row[0], text=row[1], time=row[2]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/backup')
def backup():
	backup_diary.backup(g.db)
	flash('All entries have been backed up')
	return redirect(url_for('show_entries'))

@app.route('/del_entry/<time>')
def del_entry(time):
	g.db.execute('delete from entries where time=?', (time, ))
	g.db.commit()
	flash('Post has been deleted') 
	return redirect(url_for('show_entries'))

@app.route('/add_entry', methods=['POST', 'GET'])
def add_entry():
    if session.get('logged_in'):
        if request.method == 'POST':
            g.db.execute('insert into entries (title, text, time) values (?, ?, ?)',
                    [request.form['title'], request.form['text'],
                        unicode(datetime.today())])
            g.db.commit()
            flash('New entry was posted successfully')
            return redirect(url_for('show_entries'))
        return render_template('add_entry.html')
    else:
        flash('Please log in first')
        return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            flash('logged insuccessfully')
            session['logged_in'] = True
            return redirect(url_for('show_entries'))
    if error is not None:
        flash(error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
